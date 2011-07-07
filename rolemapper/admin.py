from django.contrib import admin

from djeep.rolemapper import models
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

admin.site.register(models.HardwareInfo, HardwareInfoAdmin)


class ClusterAdmin(admin.ModelAdmin):
  list_display = ('short_name', 'display_name')

admin.site.register(models.Cluster, ClusterAdmin)


class KickTargetAdmin(admin.ModelAdmin):
  list_display = ('name', 'pxeconfig', 'preseed')

admin.site.register(models.KickTarget, KickTargetAdmin)
