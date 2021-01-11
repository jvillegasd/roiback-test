from . import forms
from . import models

from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import CreateView, ListView, DetailView
from django.views.generic.base import TemplateView

from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm

from django.contrib.auth.mixins import LoginRequiredMixin

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


class CreatePostView(LoginRequiredMixin, CreateView):
  form_class = forms.PostForm
  template_name = "blog/create_post.html"
  success_url = reverse_lazy("blog:home")
  
  def form_valid(self, form):
    self.object = form.save(commit=False)
    self.object.author = self.request.user
    self.object.save()
    form.save_m2m()
    return HttpResponseRedirect(self.get_success_url())


class CreateCategoryView(LoginRequiredMixin, CreateView):
  form_class = forms.CategoryForm
  template_name = "blog/create_category.html"
  success_url = reverse_lazy("blog:home")


class PostView(DetailView):
  model = models.Post
  template_name = "blog/view_post.html"