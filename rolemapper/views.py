import logging
import os

from django import forms
from django import http
from django import template
from django.conf import settings
from django.template import loader

from bleep.rolemapper import models
from bleep.rolemapper import static
from bleep.rolemapper import sync


class EditForm(forms.Form):
  content = forms.CharField(
      widget=forms.Textarea(attrs={'rows': 60, 'cols': 80}))
  path = forms.CharField(max_length=100, widget=forms.HiddenInput)


def home(request):
  c = template.RequestContext(request, locals())
  t = loader.get_template('home.html')
  return http.HttpResponse(t.render(c))


def flat_index(request, kind):
  if request.POST:
    name = request.POST.get('name')
    return http.HttpResponseRedirect(request.build_absolute_uri() + name)

  available = static.index(kind)
  c = template.RequestContext(request, locals())
  t = loader.get_template('flat_index.html')
  return http.HttpResponse(t.render(c))


def flat_edit(request, kind, name):
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
  templatevars = models.TemplateVar.objects.all()
  site = dict((x.key, x.value) for x in templatevars)

  # lookup which preseed template to use
  host = models.HardwareInfo.objects.get(pk=system)
  kick_target = host.kick_target
  ubuntu_mirror = site.get('ubuntu_mirror', 'mirror.rackspace.com')
  ubuntu_directory = site.get('ubuntu_directory', '/ubuntu')
  root_cryptpw = site.get('root_cryptpw', '$1$5wm8ppD/$h4uMY0gPcTKRJgZHRszBk/')
  default_cryptpw = site.get('default_cryptpw', '$1$5wm8ppD/$h4uMY0gPcTKRJgZHRszBk/')
  default_username = site.get('default_username', 'demo')

  c = template.RequestContext(request, locals())
  preseed_template = loader.get_template(
      os.path.join('preseed', kick_target.preseed))
  return http.HttpResponse(preseed_template.render(c))
