from django import dispatch
from django import forms
from django.core import signals
from django.db import models

# Create your models here.

class Config(models.Model):
  key = models.CharField(max_length=80)
  value = models.TextField()
  cluster = models.ForeignKey('Cluster', blank=True, null=True)
  description = models.TextField(blank=True)

  def __str__(self):
    return self.key


class Cluster(models.Model):
  short_name = models.CharField(max_length=40)
  display_name = models.CharField(max_length=80)

  def __str__(self):
    return self.display_name


class Host(models.Model):
  mac_address = models.CharField(max_length=80, unique=True)

  # TODO(termie): ipv6
  ip_address = models.CharField(max_length=16, unique=True)
  netmask = models.CharField(max_length=16)
  gateway = models.CharField(max_length=16)
  hostname = models.CharField(max_length=255, unique=True)
  netmask = models.CharField(max_length=16)

  state = models.CharField(max_length=255,
                           default='unmanaged',
                           choices=(('managed', 'managed'),
                                    ('unmanaged', 'unmanaged')))

  role = models.ForeignKey('Role')
  kick_target = models.ForeignKey('KickTarget')
  cluster = models.ForeignKey('Cluster')

  ipmi_ip = models.CharField(max_length=16, blank=True)
  mgmt_ip = models.CharField(max_length=16, blank=True)
  vmnet_ip = models.CharField(max_length=16, blank=True)

  def __str__(self):
    return self.hostname


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


class Role(models.Model):
  name = models.CharField(max_length=255)
  description = models.TextField()

  def __str__(self):
    return self.name


class RoleMap(models.Model):
  """Maps roles to actual puppet classes."""

  role = models.ForeignKey('Role')
  name = models.CharField(max_length=255)

  def __str__(self):
    return self.name

