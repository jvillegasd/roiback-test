from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View
from django.views.generic.base import TemplateView

from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm


# Create your views here.
class IndexView(TemplateView):
  template_name = "blog/index.html"
