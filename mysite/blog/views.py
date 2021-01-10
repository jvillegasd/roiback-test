from . import forms

from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import CreateView
from django.views.generic.base import TemplateView

from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm

from django.urls import reverse_lazy


# Create your views here.
class IndexView(TemplateView):
  template_name = "blog/index.html"


class SignupView(CreateView):
  form_class = forms.SignupForm
  template_name = "blog/sign_up.html"
  success_url = reverse_lazy("sign_in")