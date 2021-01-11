from . import forms
from . import models

from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import CreateView, ListView
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
  success_url = reverse_lazy("blog:sign_in")


class HomeView(ListView):
  model = models.Post
  template_name = "blog/home.html"


class CreatePostView(CreateView):
  # model = models.Post
  form_class = forms.PostForm
  template_name = "blog/create_post.html"
  success_url = reverse_lazy("blog:home")
  # fields = "__all__"


class CreateCategoryView(CreateView):
  form_class = forms.CategoryForm
  template_name = "blog/create_category.html"
  success_url = reverse_lazy("blog:home")