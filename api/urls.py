from django.conf.urls.defaults import patterns, include, url
from django.views.decorators import csrf

from djeep.api import resource
from djeep.api import handlers


host_handler = resource.Resource(handlers.HostHandler)
host_handler = csrf.csrf_exempt(host_handler)

kick_handler = resource.Resource(handlers.KickTargetHandler)
kick_handler = csrf.csrf_exempt(kick_handler)

puppet_handler = resource.Resource(handlers.PuppetHandler)
puppet_handler = csrf.csrf_exempt(puppet_handler)

cluster_handler = resource.Resource(handlers.ClusterHandler)
cluster_handler = csrf.csrf_exempt(cluster_handler)

urlpatterns = patterns('',
    url(r'^cluster/(?P<id>\d+)$', cluster_handler),
    url(r'^host/(?P<id>\d+)/puppet_sig$', puppet_handler),
    url(r'^host/(?P<id>\d+)$', host_handler),
    url(r'^host/', host_handler),
    url(r'^kick/(?P<id>\d+)$', kick_handler),
    url(r'^kick/', kick_handler),
)
