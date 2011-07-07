from django.contrib import admin

from bleep.rolemapper import models
from bleep.rolemapper import sync


class TemplateVarAdmin(admin.ModelAdmin):
  pass

admin.site.register(models.TemplateVar, TemplateVarAdmin)


class HardwareInfoAdmin(admin.ModelAdmin):
  pass

admin.site.register(models.HardwareInfo, HardwareInfoAdmin)


class ClusterAdmin(admin.ModelAdmin):
  pass

admin.site.register(models.Cluster, ClusterAdmin)


class KickTargetAdmin(admin.ModelAdmin):
  list_display = ('name', 'pxeconfig', 'preseed')


admin.site.register(models.KickTarget, KickTargetAdmin)
