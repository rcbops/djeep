from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.conf import settings
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'djeep.rolemapper.views.home', name='home'),
    # url(r'^djeep/', include('djeep.foo.urls')),

    url(r'^preseed/(?P<system>\d+)$', 'djeep.rolemapper.views.preseed',
        name='preseed'),
    url(r'^post_script/(?P<system>\d+)$', 'djeep.rolemapper.views.post_script',
        name='post_script'),
    url(r'^firstboot/(?P<system>\d+)$', 'djeep.rolemapper.views.firstboot',
        name='firstboot'),

    url(r'^flat/(?P<kind>[^/]+)/$', 'djeep.rolemapper.views.flat_index',
        name='flat_index'),
    url(r'^flat/(?P<kind>[^/]+)/(?P<name>[^/]+)$',
        'djeep.rolemapper.views.flat_edit',
        name='flat_edit'),

    # Include the API
    url(r'^api/', include('djeep.api.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),


    # Handling for static media
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
    }),

)
urlpatterns += patterns('django.contrib.staticfiles.views',
                        url(r'^static/(?P<path>.*)$', 'serve'))
