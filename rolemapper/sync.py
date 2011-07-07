import functools
import os

from django import template
from django.conf import settings
from django.template import loader
from django.db.models import signals

from djeep.rolemapper import models


# I handle writing the files to disk that need to be kept in sync with our db

def _ensure_dir(d):
  try:
    os.makedirs(d)
  except os.error:
    pass


def _write_pxelinux(outdir=settings.PXELINUX):
  _ensure_dir(outdir)
  templatevars = models.TemplateVar.objects.all()
  site = dict((x.key, x.value) for x in templatevars)
  for host in models.HardwareInfo.objects.all():
    pxeconfig = host.kick_target.pxeconfig

    c = template.Context(locals())
    t = loader.get_template(os.path.join('pxeconfig', pxeconfig))
    outfile = '01-%s' % (host.mac_address.replace(':', '-').lower())
    with open('%s/%s' % (outdir, outfile), 'w') as out:
      out.write(t.render(c))


def _write_dnsmasq_conf(outdir=settings.ETC):
  _ensure_dir(outdir)
  templatevars = models.TemplateVar.objects.all()
  site = dict((x.key, x.value) for x in templatevars)
  tftproot = settings.TFTPROOT

  c = template.Context(locals())
  t = loader.get_template(os.path.join('etc', 'dnsmasq.conf'))
  outfile = os.path.join(outdir, 'dnsmasq.conf')
  with open(outfile, 'w') as out:
    out.write(t.render(c))


def _write_dnsmasq_ethers(outdir=settings.ETC):
  _ensure_dir(outdir)
  templatevars = models.TemplateVar.objects.all()
  site = dict((x.key, x.value) for x in templatevars)
  hosts = models.HardwareInfo.objects.all()

  c = template.Context(locals())
  t = loader.get_template(os.path.join('etc', 'ethers'))
  outfile = os.path.join(outdir, 'ethers')
  with open(outfile, 'w') as out:
    out.write(t.render(c))


def _write_dnsmasq_hosts(outdir=settings.ETC):
  _ensure_dir(outdir)
  templatevars = models.TemplateVar.objects.all()
  site = dict((x.key, x.value) for x in templatevars)
  hosts = models.HardwareInfo.objects.all()

  c = template.Context(locals())
  t = loader.get_template(os.path.join('etc', 'hosts'))
  outfile = os.path.join(outdir, 'hosts')
  with open(outfile, 'w') as out:
    out.write(t.render(c))


def sync_to_disk(sender, instance, created=None, raw=None, using=None, **kwargs):
  """Do the work to make sure our changes are synced to disk."""
  _write_pxelinux()
  _write_dnsmasq_conf()
  _write_dnsmasq_ethers()
  _write_dnsmasq_hosts()


signals.post_save.connect(sync_to_disk)
signals.post_delete.connect(sync_to_disk)

