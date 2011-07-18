import logging
import os

from django import forms
from django import http
from django import template
from django.conf import settings
from django.template import loader

from djeep.rolemapper import models
from djeep.rolemapper import static
from djeep.rolemapper import sync


from django.contrib.auth.decorators import login_required


class EditForm(forms.Form):
  content = forms.CharField(
      widget=forms.Textarea(attrs={'rows': 60, 'cols': 80}))
  path = forms.CharField(max_length=100, widget=forms.HiddenInput)


@login_required
def home(request):
  clusters = models.Cluster.objects.all()
  for c in clusters:
    c.hosts = sorted(list(c.host_set.all()), key=lambda x: x.hostname)


  c = template.RequestContext(request, locals())
  t = loader.get_template('home.html')
  return http.HttpResponse(t.render(c))


@login_required
def flat_index(request, kind):
  """List flat files on disk."""
  if request.POST:
    name = request.POST.get('name')
    return http.HttpResponseRedirect(request.build_absolute_uri() + name)

  available = static.index(kind)
  c = template.RequestContext(request, locals())
  t = loader.get_template('flat_index.html')
  return http.HttpResponse(t.render(c))


@login_required
def flat_edit(request, kind, name):
  """Edit an arbitrary file on disk."""
  # TODO(termie): ridiculous security hole
  source, path = static.read(kind, name)

  if request.POST:
    form = EditForm(request.POST)
    try:
      if not form.is_valid():
        print "FOO"
        raise Exception('invalid form')
      data = form.clean()
      static.write(data['path'], data['content'])
      return http.HttpResponseRedirect(request.build_absolute_uri())
    except Exception:
      logging.exception("dang")
      pass
  else:
    form = EditForm(initial={'content': source, 'path': path})

  c = template.RequestContext(request, locals())
  t = loader.get_template('flat_edit.html')
  return http.HttpResponse(t.render(c))


def preseed(request, system):
  """Provide the preseed file for a given instance."""
  templatevars = models.Config.objects.all()
  site = dict((x.key, x.value) for x in templatevars)

  # lookup which preseed template to use
  host = models.Host.objects.get(pk=system)
  kick_target = host.kick_target

  # TODO(termie): the defaults should probably be in settings.py
  ubuntu_mirror = site.get('ubuntu_mirror', 'mirror.rackspace.com')
  ubuntu_directory = site.get('ubuntu_directory', '/ubuntu')
  root_cryptpw = site.get('root_cryptpw', '$1$5wm8ppD/$h4uMY0gPcTKRJgZHRszBk/')
  default_cryptpw = site.get('default_cryptpw', '$1$5wm8ppD/$h4uMY0gPcTKRJgZHRszBk/')
  default_username = site.get('default_username', 'demo')

  c = template.RequestContext(request, locals())
  preseed_template = loader.get_template(
      os.path.join('preseed', kick_target.preseed))
  return http.HttpResponse(preseed_template.render(c),
                           mimetype='text/plain',
                           content_type='text/plain')


def firstboot(request, system):
  """Provide the firstboot file for a given instance."""
  templatevars = models.Config.objects.all()
  site = dict((x.key, x.value) for x in templatevars)

  # lookup which preseed template to use
  host = models.Host.objects.get(pk=system)
  kick_target = host.kick_target

  c = template.RequestContext(request, locals())
  firstboot_template = loader.get_template(
      os.path.join('firstboot', kick_target.firstboot))
  return http.HttpResponse(firstboot_template.render(c),
                           mimetype='text/plain',
                           content_type='text/plain')


def post_script(request, system):
  """Provide the post_script file for a given instance."""
  templatevars = models.Config.objects.all()
  site = dict((x.key, x.value) for x in templatevars)

  # lookup which preseed template to use
  host = models.Host.objects.get(pk=system)
  kick_target = host.kick_target

  c = template.RequestContext(request, locals())
  post_template = loader.get_template(
      os.path.join('post_script', kick_target.post_script))
  return http.HttpResponse(post_template.render(c),
                           mimetype='text/plain',
                           content_type='text/plain')
