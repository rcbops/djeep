from django import dispatch
from django.core import signals
from django.db import models

# Create your models here.

class TemplateVar(models.Model):
  key = models.CharField(max_length=80, unique=True)
  value = models.TextField()

  def __str__(self):
    return self.key


class HardwareInfo(models.Model):
  mac_address = models.CharField(max_length=80, unique=True)
  hardware_info = models.TextField(blank=True)

  # TODO(termie): ipv6
  ip_address = models.CharField(max_length=16, unique=True)
  netmask = models.CharField(max_length=16)
  gateway = models.CharField(max_length=16)
  hostname = models.CharField(max_length=255, unique=True)
  netmask = models.CharField(max_length=16)

  role = models.CharField(max_length=80)
  state = models.CharField(max_length=255, default='unmanaged')

  kick_target = models.ForeignKey('KickTarget')
  cluster = models.ForeignKey('Cluster')

  ipmi_ip = models.CharField(max_length=16, blank=True)

  def __str__(self):
    return self.hostname


class Cluster(models.Model):
  short_name = models.CharField(max_length=40)
  display_name = models.CharField(max_length=80)

  def __str__(self):
    return self.display_name


class KickTarget(models.Model):
  name = models.CharField(max_length=40)
  pxeconfig = models.CharField(max_length=40)
  kernel = models.CharField(max_length=255, blank=True)
  initrd = models.CharField(max_length=255, blank=True)
  preseed = models.CharField(max_length=255, blank=True)
  post_script = models.CharField(max_length=255, blank=True)
  firstboot = models.CharField(max_length=255, blank=True)

  def __str__(self):
    return self.name
