from django import forms
from django import shortcuts
from django.contrib import admin
from django.contrib import messages
from django.db import models as django_models

from djeep.rolemapper import models
from djeep.rolemapper import remote
from djeep.rolemapper import sync


class ConfigAdmin(admin.ModelAdmin):
  list_display = ('key', 'value', 'cluster')
  list_editable = ('value', 'cluster')
  list_filter = ('cluster', )
  ordering = ('key',)
  formfield_overrides = {
      django_models.TextField: {'widget': forms.TextInput(attrs={'size': 100})}
  }

  def clone_config(modeladmin, request, queryset):
    clone_to = request.POST.get('clone_to')
    if not clone_to:
      messages.error(request, "Please specifiy a Cluster Name")
    else:
      cluster = models.Cluster.objects.filter(short_name__exact=clone_to)
      if cluster:
        cluster = cluster[0]
        for config in queryset:
          previous = models.Config.objects.filter(cluster__exact=cluster.id,
                                                  key__exact=config.key)
          if not previous:
            config.id = None
            config.cluster = cluster
            config.save()
            messages.info(request, "Config %s added to %s(%s)" %
                                   (config.key, cluster.short_name, cluster.id))
          else:
            messages.info(request, "Config %s already exists for %s(%s)" %
                                   (config.key, cluster.short_name, cluster.id))
        return shortcuts.redirect(request.build_absolute_uri() +
                                  ("?cluster__id__exact=%s" % cluster.id))
      else:
        messages.error(request, "Cluster '%s' not found" % clone_to)
      pass

  clone_config.short_description = 'Clone selected configs to other cluster'
  actions = [clone_config]

admin.site.register(models.Config, ConfigAdmin)


class ClusterAdmin(admin.ModelAdmin):
  list_display = ('short_name', 'display_name')
  list_editable = ('display_name',)

admin.site.register(models.Cluster, ClusterAdmin)


class HostAdmin(admin.ModelAdmin):
  list_display = ('hostname',
                  'ip_address',
                  'ipmi_ip_link',
                  'mac_address',
                  'role',
                  'state',
                  'kick_target',
                  'cluster')
  list_editable = ('kick_target', 'role')
  list_filter = ('cluster',)
  ordering = ['hostname']
  actions = ['reboot']

  def ipmi_ip_link(self, inst):
    return '<a href="http://%s">%s</a>' % (inst.ipmi_ip, inst.ipmi_ip)

  ipmi_ip_link.allow_tags = True
  ipmi_ip_link.admin_order_field = 'ipmi_ip'
  ipmi_ip_link.short_description = 'ipmi_ip'

  def reboot(self, request, queryset):
    for host in queryset:
      remote.reboot(host)

    self.message_user(request, 'Rebooted %s machines.' % len(queryset))

  reboot.short_description = 'Reboot selected host'

admin.site.register(models.Host, HostAdmin)


class KickTargetAdmin(admin.ModelAdmin):
  list_display = ('name', 'pxeconfig', 'preseed')

admin.site.register(models.KickTarget, KickTargetAdmin)


class RoleAdmin(admin.ModelAdmin):
  list_display = ('id', 'name', 'description')
  list_editable = ('name', )

admin.site.register(models.Role, RoleAdmin)


class RoleMapAdmin(admin.ModelAdmin):
  list_display = ('id', 'role', 'name')
  list_editable = ('role', 'name')

admin.site.register(models.RoleMap, RoleMapAdmin)
