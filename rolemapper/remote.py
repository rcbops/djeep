import logging
import subprocess

from django.conf import settings


def _build_ipmi_command(host, *args):
  command = ['/usr/bin/ipmitool',
             '-H', host.ipmi_ip,
             '-U', settings.IPMI_USER,
             '-P', settings.IPMI_PASSWORD] + args


def reboot(host):
  command = _build_ipmi_command(host, 'power', 'cycle')
  logging.info('Rebooting: %s', host.hostname)
  try:
    subprocess.check_call(command)
  except Exception:
    logging.exception('in reboot host: %s', host.hostname)


def pxe_reboot(host):
  command = _build_ipmi_command(host, 'chassis', 'bootdev', 'pxe')
  logging.info('Setting PXE Boot for: %s', host.hostname)
  try:
    subprocess.check_call(command)
  except Exception:
    logging.exception('in reboot host: %s', host.hostname)

  reboot(host)
