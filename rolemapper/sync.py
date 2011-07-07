import os

from django import template
from django.conf import settings
from django.template import loader
from django.db.models import signals

from bleep.rolemapper import models


def _write_pxelinux(outdir=settings.PXELINUX):
  templatevars = models.TemplateVar.objects.all()

  site = dict((x.key, x.value) for x in templatevars)
  for host in models.HardwareInfo.objects.all():
    pxeconfig = host.kick_target.pxeconfig

    c = template.Context(locals())
    t = loader.get_template(os.path.join('pxeconfig', pxeconfig))

    outfile = '01-%s' % (host.mac_address.replace(':', '-').lower())
    with open('%s/%s' % (outdir, outfile), 'w') as out:
      out.write(t.render(c))


def sync_to_disk(sender, instance, created=None, raw=None, using=None, **kwargs):
  """Do the work to make sure our changes are synced to disk."""
  _write_pxelinux()


signals.post_save.connect(sync_to_disk)
signals.post_delete.connect(sync_to_disk)

