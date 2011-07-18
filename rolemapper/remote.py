import logging
import subprocess

from django.conf import settings


def reboot(host):
  command = ['/usr/bin/ipmitool',
             '-H', host.ip_address,
             '-U', settings.IPMI_USER,
             '-P', settings.IPMI_PASSWORD,
             'power', 'cycle']
  logging.info('Rebooting: %s', host.hostname)
  try:
    subprocess.check_call(command)
  except Exception:
    logging.exception('in reboot host: %s', host.hostname)
