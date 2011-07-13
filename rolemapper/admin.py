from django import forms
from django.contrib import admin
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
