from django.conf.urls.defaults import patterns, include, url
from django.views.decorators import csrf

from piston import resource
from djeep.api import handlers


hardware_handler = resource.Resource(handlers.HardwareInfoHandler)
hardware_handler = csrf.csrf_exempt(hardware_handler)

urlpatterns = patterns('',
    url(r'^hardware/(?P<id>\d+)', hardware_handler),
    url(r'^hardware/', hardware_handler),
)
