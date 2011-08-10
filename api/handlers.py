import logging
import subprocess

import eventlet
from django.core import exceptions
from piston import handler
from piston.utils import rc

from rolemapper import models
from rolemapper import remote

#class BaseHandler(handler.BaseHandler):
#  def update(self, request, *args, **kwargs):
#    if not self.has_model():
#      return rc.NOT_IMPLEMENTED

#    pkfield = self.model._meta.pk.name

#    if pkfield not in kwargs:
#      # No pk was specified
#      return rc.BAD_REQUEST

#    try:
#      inst = self.queryset(request).get(pk=kwargs.get(pkfield))
#    except exceptions.ObjectDoesNotExist:
#      return rc.NOT_FOUND
#    except exceptions.MultipleObjectsReturned:
#      return rc.BAD_REQUEST

#    attrs = self.flatten_dict(request.data)
#    print attrs
#    for k,v in attrs.iteritems():
#      setattr(inst, k, v)

#    inst.save()
#    return rc.ALL_OK


class HostHandler(handler.BaseHandler):
  allowed_methods = ('GET', 'PUT')
  model = models.Host


class PuppetHandler(handler.BaseHandler):
  allowed_methods = ('DELETE',)

  def delete(self, request, id):
    host = models.Host.objects.get(pk=id)
    command = ['/usr/sbin/puppetca', '--clean', host.hostname]
    try:
      subprocess.check_call(command)
    except Exception:
      logging.exception('in subprocess call:')
    return {}


class ClusterHandler(handler.BaseHandler):
  allowed_methods = ('BREW',)

  def brew(self, request, id):
    """Redeploy a cluster."""
    cluster = models.Cluster.objects.get(pk=id)
    hosts = models.Host.objects.filter(cluster=cluster)

    for host in hosts:
      host.local_boot =  False
      host.save()
      remote.pxe_reboot(host)

    return {}
