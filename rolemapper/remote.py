import logging
import subprocess
from views import _get_site_config
from django.conf import settings


def _build_ipmi_command(host, *args):
  config = _get_site_config(host)
  user = config.get('ipmi_user', settings.IPMI_USER)
  password = config.get('ipmi_password', settings.IPMI_PASSWORD)
  
  return  ['/usr/bin/ipmitool',
           '-I', 'lanplus',
           '-H', host.ipmi_ip,
           '-U', user,
           '-P', password] + list(args)


def reboot(host):
  # 'reset' performs a cold reboot, which is necessary for pxe booting to work
  # 'cycle' was not sufficient
  command = _build_ipmi_command(host, 'power', 'reset')
  logging.info('Rebooting: %s', host.hostname)
  logging.debug("Using command %s" % command)

  try:
    subprocess.check_call(command)
  except Exception:
    logging.exception('in reboot host: %s', host.hostname)


def pxe_reboot(host):
  command = _build_ipmi_command(host, 'chassis', 'bootdev', 'pxe')
  logging.info('Setting PXE Boot for: %s', host.hostname)
  logging.debug("Using command %s" % command)
  try:
    subprocess.check_call(command)
  except Exception:
    logging.exception('in pxe_reboot host: %s', host.hostname)

  reboot(host)
