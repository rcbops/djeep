import os

from django.conf import settings

# I make static files look like something that can be edited.
# Someday I will be part of the admin interface and look pretty.


# I only care about one template directory
TEMPLATE_DIR = settings.TEMPLATE_DIRS[0]


# steal the django template loading logic to get at our files
#def get_template_source(template_name):
#  template_source_loaders = loader.template_source_loaders
#  for l in loader.template_source_loaders:
#    try:
#      return l.load_template_source(template_name)
#    except Exception:
#      pass
#  raise Exception('Failed to load template source')


def sync():
  # using all the information available, write the appropriate information
  # to all the places they need to be written
  pass


def index(prefix):
  l = os.listdir(os.path.join(TEMPLATE_DIR, prefix))
  return l


def read(prefix, name):
  path = os.path.normpath(os.path.join(TEMPLATE_DIR, prefix, name))
  try:
    source = open(path).read()
  except Exception:
    source = ''
  return source, path


def write(path, content):
  print path
  f = open(path, 'w')
  f.write(content)
  f.close()
