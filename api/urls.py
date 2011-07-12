from django.conf.urls.defaults import patterns, include, url
from django.views.decorators import csrf

from piston import resource
from djeep.api import handlers


host_handler = resource.Resource(handlers.HostHandler)
host_handler = csrf.csrf_exempt(host_handler)

urlpatterns = patterns('',
    url(r'^host/(?P<id>\d+)', host_handler),
    url(r'^host/', host_handler),
)
