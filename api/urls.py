from django.conf.urls.defaults import patterns, include, url
from django.views.decorators import csrf

from djeep.api import resource
from djeep.api import handlers


host_handler = resource.Resource(handlers.HostHandler)
host_handler = csrf.csrf_exempt(host_handler)

host_kicker = resource.Resource(handlers.HostKicker)
host_kicker = csrf.csrf_exempt(host_kicker)

host_rebooter = resource.Resource(handlers.HostRebooter)
host_rebooter = csrf.csrf_exempt(host_rebooter)

kick_handler = resource.Resource(handlers.KickTargetHandler)
kick_handler = csrf.csrf_exempt(kick_handler)

puppet_handler = resource.Resource(handlers.PuppetHandler)
puppet_handler = csrf.csrf_exempt(puppet_handler)

cluster_handler = resource.Resource(handlers.ClusterHandler)
cluster_handler = csrf.csrf_exempt(cluster_handler)

cluster_claim_handler = resource.Resource(handlers.ClusterClaimHandler)
cluster_claim_handler = csrf.csrf_exempt(cluster_claim_handler)

cluster_status_handler = resource.Resource(handlers.ClusterStatusHandler)
cluster_status_handler = csrf.csrf_exempt(cluster_status_handler)

urlpatterns = patterns('',
    url(r'^cluster/claim/(?P<claim>[^/]*)/prefix/(?P<prefix>[^/]+)/?$',
        cluster_claim_handler),
    url(r'^cluster/claim/(?P<claim>[^/]*)(/(?P<name>[^/]+)?)?/?$',
        cluster_claim_handler),
    url(r'^clusters/?', cluster_status_handler, {'emitter_format': 'json'}),
    url(r'^clusterbyname/(?P<name>[^/]+)$', cluster_handler),
    url(r'^cluster/(?P<id>\d+)$', cluster_handler),
    url(r'^host/(?P<id>\d+)/rekick$', host_kicker),
    url(r'^hostbyname/(?P<name>[^/]+)/rekick$', host_kicker),
    url(r'^host/(?P<id>\d+)/reboot$', host_rebooter),
    url(r'^hostbyname/(?P<name>[^/]+)/reboot$', host_rebooter),
    url(r'^host/(?P<id>\d+)/puppet_sig$', puppet_handler),
    url(r'^host/(?P<id>\d+)$', host_handler),
    url(r'^host/', host_handler),
    url(r'^kick/(?P<id>\d+)$', kick_handler),
    url(r'^kick/', kick_handler),
)
