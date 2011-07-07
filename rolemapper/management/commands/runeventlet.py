import eventlet
eventlet.monkey_patch()

from eventlet import wsgi
from django.core.management.commands import runserver


class Command(runserver.Command):
  args = '[optional port numer, or ipaddr:port]'
  help = 'Starts a webserver using eventlet and wsgi'

  def run(self, *args, **options):
    handler = self.get_handler(*args, **options)
    wsgi.server(eventlet.listen((self.addr, int(self.port))), handler)
