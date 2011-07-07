from django.contrib import admin

from djeep.rolemapper import models
from djeep.rolemapper import remote
from djeep.rolemapper import sync


class TemplateVarAdmin(admin.ModelAdmin):
  pass

admin.site.register(models.TemplateVar, TemplateVarAdmin)


class HardwareInfoAdmin(admin.ModelAdmin):
  list_display = ('hostname',
                  'ip_address',
                  'mac_address',
                  'role',
                  'state',
                  'kick_target',
                  'cluster')

  actions = ['reboot']
  def reboot(self, request, queryset):
    for hardware in queryset:
      remote.reboot(hardware)

    self.message_user(request, 'Rebooted %s machines.' % len(queryset))

  reboot.short_description = 'Reboot selected hardware'

admin.site.register(models.HardwareInfo, HardwareInfoAdmin)


class ClusterAdmin(admin.ModelAdmin):
  list_display = ('short_name', 'display_name')

admin.site.register(models.Cluster, ClusterAdmin)


class KickTargetAdmin(admin.ModelAdmin):
  list_display = ('name', 'pxeconfig', 'preseed')

admin.site.register(models.KickTarget, KickTargetAdmin)
