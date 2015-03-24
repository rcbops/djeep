import logging
import subprocess

import eventlet
from django.db import transaction
from django.core import exceptions
from piston import handler
from piston import utils
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
    exclude = ()
    allowed_methods = ('GET', 'PUT')
    model = models.Host

class HostKicker(handler.BaseHandler):
    allowed_methods = ('POST',)

    def host_from_kwargs(self, kwargs):
        query = {}
        if 'id' in kwargs:
            query['pk'] = kwargs['id']
        elif 'name' in kwargs:
            query['hostname__exact'] = kwargs['name']

        host = models.Host.objects.get(**query)
        return host

    def create(self, request, **kwargs):
        """ Rekick a single host """
        host = self.host_from_kwargs(kwargs)
        host.local_boot = False
        host.save()
        remote.pxe_reboot(host)

class HostRebooter(HostKicker):

    def create(self, request, **kwargs):
        """ Reboot a single host """
        host = self.host_from_kwargs(kwargs)
        remote.reboot(host)


class KickTargetHandler(handler.BaseHandler):
    exclude = ()
    allowed_methods = ('GET', 'PUT')
    model = models.KickTarget


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

class ClusterClaimHandler(handler.BaseHandler):
    """ API Methods for reservation system

        POST actions:
        claim with cluster name: claims cluster if available
        claim without cluster name: claim next available cluster
        claim with prefix: claim next avilable cluster matching prefix

        DELETE actions:
        release cluster with name and prefix: Releases claim by setting
            claim field to empty string.

        Note: This handler only creates/deletes claims.
        It doesn't create/delete clusters.
    """
    allowed_methods = ('POST', 'DELETE')

    def create(self, request, **kwargs):
        with transaction.commit_manually():
            self.cluster = None
            data = kwargs
            if data.get('name'):
                try:
                    self.cluster = models.Cluster.objects.get(
                        short_name__exact=data['name'])
                except exceptions.ObjectDoesNotExist as e:
                    resp = rc.NOT_FOUND
                    resp.content = ('Cluster %(name)s not found. Error: %(e)s' %
                            {'name': data['name'], 'e':e})
                    transaction.rollback()
                    return resp
                else:
                    if self.cluster.claim not in ['', data['claim']]:
                        resp = rc.FORBIDDEN
                        resp.content = ('Cluster %(cluster)s is already claimed: '
                                        '%(claim)s' %
                                            {'cluster': self.cluster.short_name,
                                            'claim': self.cluster.claim}
                                    )
                        transaction.rollback()
                        return resp
            else:
                query = {'claim__exact': ''}
                if data.get('prefix'):
                    query['short_name__startswith']=data['prefix']
                available_clusters = models.Cluster.objects.filter(**query)
                if not available_clusters:
                    resp = rc.THROTTLED
                    resp.content = 'No clusters are available :('
                    transaction.rollback()
                    return resp
                self.cluster = available_clusters[0]

            # At this point we have either returned due to failure, or have a
            # cluster via name, prefix or allocation.
            self.cluster.claim = data['claim']
            self.cluster.save()
            transaction.commit()
            resp = rc.CREATED
            resp.content = ('Cluster %(cluster)s claimed with '
                            'string %(claim)s' %
                                {'cluster': self.cluster.short_name,
                                'claim': self.cluster.claim}
                            )
            return resp

    def delete(self, request, **kwargs):
        self.cluster = None
        data = kwargs
        try:
            self.cluster = models.Cluster.objects.get(
                short_name__exact=data['name'])
            if self.cluster.claim == data['claim']:
                self.cluster.claim = ''
                self.cluster.save()
                resp = rc.DELETED
                return resp
            else:
                resp = rc.FORBIDDEN
                resp.content = ('Cant release cluster %(cluster)s, incorrect'
                                ' claim supplied. Current claim:  %(claim)s'
                                ' Supplied: %(req_claim)s' %
                                    {'cluster': self.cluster.short_name,
                                    'claim': self.cluster.claim,
                                    'req_claim': data['claim']}
                            )
                return resp
        except exceptions.ObjectDoesNotExist as e:
            resp = rc.NOT_FOUND
            resp.content = ('Cluster %(name)s not found. Error: %(e)s' %
                            {'name': data['name'],
                             'e': e})
            return resp

class ClusterStatusHandler(handler.BaseHandler):
    allowed_methods = ('GET',)

    def read(self, request, **kwargs):
        return models.Cluster.objects.all()


class ClusterHandler(handler.BaseHandler):
    allowed_methods = ('BREW', 'POST')

    def create(self, request, **kwargs):
        self.brew(request, **kwargs)

    def brew(self, request, **kwargs):
        """Redeploy a cluster."""

        query = {}
        if 'id' in kwargs:
            query['pk'] = kwargs['id']
        elif 'name' in kwargs:
            query['short_name__exact'] = kwargs['name']

        cluster = models.Cluster.objects.get(**query)

        hosts = models.Host.objects.filter(cluster=cluster)

        # TODO(termie): A bit of a hack because I don't want to replicate the
        #               entire __call__ method in piston's Resource.
        try:
            utils.translate_mime(request)
        except utils.MimerDataException:
            return rc.BAD_REQUEST

        request.data = getattr(request, 'data', None)
        if cluster.claim and (not request.data or
                              cluster.claim != request.data.get('claim')):
            resp = rc.FORBIDDEN
            resp.content = ('FORBIDDEN: This cluster has been claimed: %s'
                            % cluster.claim)
            return resp

        for host in hosts:
            host.local_boot = False
            host.save()
            remote.pxe_reboot(host)

        return hosts
