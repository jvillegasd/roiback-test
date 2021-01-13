from . import forms
from . import models
from django.template import loader
from django.urls import reverse_lazy, reverse
from django.contrib.auth import login, logout
from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView
from django.core.exceptions import PermissionDenied
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import CreateView, ListView, DetailView, UpdateView


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

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["categories"] = models.Category.objects.all()
    context["authors"] = models.User.objects.filter(blog_posts__isnull=False).distinct("username")
    context["tags"] = models.Tag.objects.all()
    
    return context


class CreatePostView(LoginRequiredMixin, CreateView):
  form_class = forms.PostForm
  template_name = "blog/create_post.html"
  success_url = reverse_lazy("blog:home")
  
  def form_valid(self, form):
    tags = form.cleaned_data["tag"]
    self.object = form.save(commit=False)
    self.object.author = self.request.user
    self.object.save()
    
    if tags:
      self.object.tags.add(*tags)
    return HttpResponseRedirect(self.get_success_url())


class EditPostView(LoginRequiredMixin, UpdateView):
  model = models.Post
  form_class = forms.PostForm
  template_name = "blog/edit_post.html"

  def dispatch(self, request, *args, **kwargs):
    handler = super().dispatch(request, *args, **kwargs)
    
    if not (self.request.user == self.object.author or self.request.user.is_superuser):
      raise PermissionDenied
    return handler

  def get_success_url(self):
    return reverse("blog:view_post", kwargs={"slug": self.object.slug})
  
  def form_valid(self, form):
    tags = form.cleaned_data["tag"]
    self.object = form.save(commit=False)
    self.object.author = self.request.user
    self.object.save()
    
    if tags:
      self.object.tags.add(*tags)
    return HttpResponseRedirect(self.get_success_url())


class PostView(DetailView):
  model = models.Post
  template_name = "blog/view_post.html"

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["comment_form"] = forms.CommentForm
    liked_post = False

    if self.request.user.is_authenticated:
      liked_post = self.request.user.likes.filter(slug=self.kwargs["slug"]).exists()
    
    context["liked_post"] = liked_post
    return context


class CreateCommentView(LoginRequiredMixin, CreateView):
  form_class = forms.CommentForm
  
  def get_success_url(self):
    return reverse("blog:view_post", kwargs={"slug": self.object.post.slug})

  def form_valid(self, form):
    post = get_object_or_404(models.Post, slug=self.kwargs["slug"])
    self.object = form.save(commit=False)
    self.object.post = post
    self.object.author = self.request.user
    self.object.save()
    
    return HttpResponseRedirect(self.get_success_url())


def LikePostView(request, slug):
  post = get_object_or_404(models.Post, slug=slug)
  post.likes.add(request.user)
  
  return HttpResponseRedirect(
    reverse("blog:view_post", kwargs={"slug": slug})
  )


def UnlikePostView(request, slug):
  post = get_object_or_404(models.Post, slug=slug)
  post.likes.remove(request.user)
  
  return HttpResponseRedirect(
    reverse("blog:view_post", kwargs={"slug": slug})
  )


class CreateCategoryView(LoginRequiredMixin, CreateView):
  form_class = forms.CategoryForm
  template_name = "blog/create_category.html"
  success_url = reverse_lazy("blog:home")


class AuthorFilterView(ListView):
  model = models.Post
  template_name = "blog/author_filter.html"

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    selected_author = get_object_or_404(models.User, username=self.kwargs["username"])

    context["filtered_posts"] = models.Post.objects.filter(author=selected_author)
    context["categories"] = models.Category.objects.all()
    context["authors"] = models.User.objects.filter(blog_posts__isnull=False).distinct("username")
    context["tags"] = models.Tag.objects.all()
    
    return context


class CategoryFilterView(ListView):
  model = models.Post
  template_name = "blog/category_filter.html"

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    selected_category = get_object_or_404(models.Category, slug=self.kwargs["slug"])

    context["filtered_posts"] = models.Post.objects.filter(category=selected_category)
    context["categories"] = models.Category.objects.all()
    context["authors"] = models.User.objects.filter(blog_posts__isnull=False).distinct("username")
    context["tags"] = models.Tag.objects.all()
    
    return context


class TagsFilterView(ListView):
  model = models.Post
  template_name = "blog/tags_filter.html"

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["filtered_posts"] = models.Post.objects.filter(tags__name__in=[self.kwargs["tag"]])
    context["categories"] = models.Category.objects.all()
    context["authors"] = models.User.objects.filter(blog_posts__isnull=False).distinct("username")
    context["tags"] = models.Tag.objects.all()
    
    return context