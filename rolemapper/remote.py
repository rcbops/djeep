import logging
import subprocess

from django.conf import settings


def _build_ipmi_command(host, *args):
  return  ['/usr/bin/ipmitool',
           '-H', host.ipmi_ip,
           '-U', settings.IPMI_USER,
           '-P', settings.IPMI_PASSWORD] + list(args)


def reboot(host):
  # 'reset' performs a cold reboot, which is necessary for pxe booting to work
  # 'cycle' was not sufficient
  command = _build_ipmi_command(host, 'power', 'reset')
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
    logging.exception('in pxe_reboot host: %s', host.hostname)

  reboot(host)
