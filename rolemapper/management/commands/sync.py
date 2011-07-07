from django.core.management import base

from djeep.rolemapper import sync

class Command(base.BaseCommand):
  args = ''
  help = 'Sync generated files to disk'

  def handle(self, *args, **options):
    sync.sync_to_disk()
