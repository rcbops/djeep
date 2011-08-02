import functools
import json
import logging
import os
import subprocess

from django import template
from django.conf import settings
from django.template import loader
from django.db.models import signals
import eventlet
from eventlet import event
from eventlet import semaphore
import paramiko

from djeep.rolemapper import models

# I handle writing the files to disk that need to be kept in sync with our db


logging = logging.getLogger(__name__)


ARBITRARY_SEMAPHORE_SIZE = 100
SYNC_EVENT = None
SYNC_LOCK = semaphore.Semaphore(ARBITRARY_SEMAPHORE_SIZE)


def _ensure_dir(d):
  try:
    os.makedirs(d)
    logging.info('Created directory: %s', d)
  except os.error:
    pass


def _write_pxelinux(outdir=settings.PXELINUX):
  _ensure_dir(outdir)
  templatevars = models.Config.objects.all()
  site = dict((x.key, x.value) for x in templatevars)
  # TODO(termie): clear out old files

  for host in models.Host.objects.all():
    pxeconfig = host.kick_target.pxeconfig

    c = template.Context(locals())
    t = loader.get_template(os.path.join('pxeconfig', pxeconfig))
    outfile = '01-%s' % (host.mac_address.replace(':', '-').lower())
    with open('%s/%s' % (outdir, outfile), 'w') as out:
      out.write(t.render(c))
      logging.info('Wrote PXE for: %s', host.hostname)


def _write_dnsmasq_conf(outdir=settings.ETC):
  _ensure_dir(outdir)
  templatevars = models.Config.objects.all()
  site = dict((x.key, x.value) for x in templatevars)
  tftproot = settings.TFTPROOT

  c = template.Context(locals())
  t = loader.get_template(os.path.join('etc', 'dnsmasq.conf'))
  outfile = os.path.join(outdir, 'dnsmasq.conf')
  with open(outfile, 'w') as out:
    out.write(t.render(c))
    logging.info('Wrote etc/dnsmasq.conf')


def _write_dnsmasq_ethers(outdir=settings.ETC):
  _ensure_dir(outdir)
  templatevars = models.Config.objects.all()
  site = dict((x.key, x.value) for x in templatevars)
  hosts = models.Host.objects.all()

  c = template.Context(locals())
  t = loader.get_template(os.path.join('etc', 'ethers'))
  outfile = os.path.join(outdir, 'ethers')
  with open(outfile, 'w') as out:
    out.write(t.render(c))
    logging.info('Wrote etc/ethers')


def _write_dnsmasq_hosts(outdir=settings.ETC):
  _ensure_dir(outdir)
  templatevars = models.Config.objects.all()
  site = dict((x.key, x.value) for x in templatevars)
  hosts = models.Host.objects.all()

  c = template.Context(locals())
  t = loader.get_template(os.path.join('etc', 'hosts'))
  outfile = os.path.join(outdir, 'hosts')
  with open(outfile, 'w') as out:
    out.write(t.render(c))
    logging.info('Wrote etc/hosts')


def _write_ssh_key(outdir=settings.SSH):
  _ensure_dir(outdir)
  outfile = os.path.join(outdir, 'id_rsa')
  outfile_public = os.path.join(outdir, 'id_rsa.pub')

  if not os.path.exists(outfile):
    private = paramiko.RSAKey.generate(1024)
    private.write_private_key_file(outfile)
    logging.info('Wrote ssh/id_rsa')
  else:
    private = paramiko.RSAKey.from_private_key_file(outfile)

  if not os.path.exists(outfile_public):
    with open(outfile_public, 'w') as out:
      out.write('%s %s' % (private.get_name(), private.get_base64()))
      logging.info('Wrote ssh/id_rsa.pub')


def _write_authorized_keys(outdir=settings.SSH):
  public_key_path = os.path.join(outdir, 'id_rsa.pub')
  public_key = open(public_key_path).read()
  command = '/sbin/shutdown -rf now'
  outfile = os.path.join(outdir, 'authorized_keys')

  if not os.path.exists(outfile):
    with open(outfile, 'w') as out:
      out.write('command="%s" %s' % (command, public_key))
      logging.info('Wrote ssh/authorized_keys')


def _write_puppet_clusters(outdir=settings.PUPPET_CLUSTERS):
  _ensure_dir(outdir)
  global_config = models.Config.objects.filter(cluster=None)
  global_config = dict((x.key, x.value) for x in global_config)

  for cluster in models.Cluster.objects.all():
    cluster_config = models.Config.objects.filter(cluster=cluster)
    cluster_config = dict((x.key, x.value) for x in cluster_config)

    options = global_config.copy()
    options.update(cluster_config)

    outfile = os.path.join(outdir, '%s' % cluster.short_name)
    with open(outfile, 'w') as out:
      out.write(json.dumps({'options': options}, indent=2))
      logging.info('Wrote Puppet cluster for: %s', cluster.short_name)


def _write_puppet_hosts(outdir=settings.PUPPET_HOSTS):
  _ensure_dir(outdir)

  role_map = models.RoleMap.objects.all()
  roles = {}
  for x in role_map:
    mapped = roles.get(x.role_id, [])
    mapped.append(x.name)
    roles[x.role_id] = mapped

  for host in models.Host.objects.all():
    classes = roles.get(host.role_id, [])
    options = {'cluster': host.cluster.short_name,
               'host_ip_address': host.ip_address,
               'host_mac_address': host.mac_address,
               'host_gateway': host.gateway,
               'host_netmask': host.netmask,
               'host_hostname': host.hostname,
               }
    outfile = os.path.join(outdir, '%s' % host.hostname)
    content = {'classes': classes,
               'options': options,
               }

    with open(outfile, 'w') as out:
      out.write(json.dumps(content, indent=2))
      logging.info('Wrote Puppet host for: %s', host.hostname)


def _kick_dnsmasq():
  command = ['/etc/init.d/dnsmasq', 'restart']
  try:
    subprocess.check_call(command)
  except Exception:
    logging.exception('in kick dnsmasq')


def sync_to_disk(sender=None, *args, **kwargs):
  """Do the work to make sure our changes are synced to disk."""
  updating_models = (models.Config,
                     models.Cluster,
                     models.Host,
                     models.KickTarget,
                     models.Role,
                     models.RoleMap)

  if sender and sender not in updating_models:
    return

  # We're adding a delay to the syncs so that if a bunch come in
  # over a short period of time we don't write to disk until at least
  # SYNC_DELAY seconds have passed.
  # To do that, we spawn a greenthread to do the syncing that will be
  # cancelled if another call is made before it starts to execute.

  global SYNC_LOCK
  global SYNC_EVENT

  already_started = False
  if SYNC_EVENT:
    logging.debug('Delaying sync_to_disk, in batched operation')
    already_started = True
  else:
    logging.debug('Starting sync_to_disk batch')
    SYNC_EVENT = event.Event()


  def _wait(sem, waiter):
    sem.acquire()
    eventlet.sleep(settings.SYNC_DELAY)
    sem.release()
    # We were the last release
    if waiter and sem.balance == ARBITRARY_SEMAPHORE_SIZE:
      waiter.send(True)

  eventlet.spawn(_wait, SYNC_LOCK, SYNC_EVENT)

  # If we've already got a sync in the pipe don't bother adding more
  if already_started:
    return

  def _do():
    global SYNC_EVENT
    SYNC_EVENT.wait()
    SYNC_EVENT = None

    _write_pxelinux()
    _write_dnsmasq_conf()
    _write_dnsmasq_ethers()
    _write_dnsmasq_hosts()
    _write_ssh_key()
    _write_authorized_keys()
    _write_puppet_clusters()
    _write_puppet_hosts()
    _kick_dnsmasq()

  eventlet.spawn(_do)

signals.post_save.connect(sync_to_disk)
signals.post_delete.connect(sync_to_disk)

