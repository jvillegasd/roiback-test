from . import forms
from . import models
from django.template import loader
from django.urls import reverse_lazy, reverse
from django.contrib.auth import login, logout
from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView
from django.core.exceptions import PermissionDenied
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView


# Create your views here.
class IndexView(TemplateView):
  """
    Index view - Show landing page
  """
  template_name = "blog/index.html"


class SignupView(CreateView):
  """
    Signup view.

    This view uses a custom sign up form.
  """
  form_class = forms.SignupForm
  template_name = "blog/sign_up.html"
  success_url = reverse_lazy("blog:sign_in")


class HomeView(ListView):
  """
    Home view.

    This List view only shows published posts from every registered users.
    A filter by Author, Category, Tag is shown for better posts search.
  """
  model = models.Post
  template_name = "blog/home.html"

  def get_context_data(self, **kwargs):
    """
      Override context_data function for custom requirements.
      New context variables created:
        - object_list: Save published posts from every registered users.
        - categories: Save created categories for filter component
        - authors: Save users who have published posts for filter component
        - tags: Save created tags
    """
    context = super().get_context_data(**kwargs)
    context["object_list"] = models.Post.objects.get_published_posts()
    context["categories"] = models.Category.objects.all()
    context["authors"] = models.User.objects.filter(blog_posts__isnull=False).distinct("username")
    context["tags"] = models.Tag.objects.all()
    
    return context


class AuthorPostsView(ListView):
  """
    Author post view.

    Show every post a user created, no matter their published status.
  """
  model = models.Post
  template_name = "blog/author_posts.html"

  def dispatch(self, request, *args, **kwargs):
    """
      Override dispatch function for security reason.
      Check if current user is accessing to their own author post view.
      A superuser can enter to every user posts.
    """
    handler = super().dispatch(request, *args, **kwargs)
    
    if not (self.request.user.username == self.kwargs["username"] or self.request.user.is_superuser):
      raise PermissionDenied
    return handler

  def get_context_data(self, **kwargs):
    """
      Override context_data function for custom requirements.
      New context variables created:
        - object_list: Save every post the current user created.
        - categories: Save created categories for filter component
        - authors: Save users who have published posts for filter component
        - tags: Save created tags
    """
    context = super().get_context_data(**kwargs)
    selected_author = get_object_or_404(models.User, username=self.kwargs["username"])

    context["object_list"] = models.Post.objects.get_posts_by_author(selected_author)
    context["categories"] = models.Category.objects.all()
    context["authors"] = models.User.objects.filter(blog_posts__isnull=False).distinct("username")
    context["tags"] = models.Tag.objects.all()
    
    return context


class CreatePostView(LoginRequiredMixin, CreateView):
  """
    Create post view.

    This Create view allows a user to create their post.
  """
  form_class = forms.PostForm
  template_name = "blog/create_post.html"
  success_url = reverse_lazy("blog:home")
  
  def form_valid(self, form):
    """
      Override form_valid function for save every tag typed by user.
      Tags is manager by Django-taggit package.
    """
    tags = form.cleaned_data["tag"]
    self.object = form.save(commit=False)
    self.object.author = self.request.user
    self.object.save()
    
    if tags:
      self.object.tags.add(*tags)
    return HttpResponseRedirect(self.get_success_url())


class EditPostView(LoginRequiredMixin, UpdateView):
  """
    Edit post view.

    This Update view allows a user to edit their post.
  """
  model = models.Post
  form_class = forms.PostForm
  template_name = "blog/edit_post.html"

  def dispatch(self, request, *args, **kwargs):
    """
      Override dispatch function for security reason.
      Check if current user is accessing to their own post.
      A superuser can edit every user posts.
    """
    handler = super().dispatch(request, *args, **kwargs)
    
    if not (self.request.user == self.object.author or self.request.user.is_superuser):
      raise PermissionDenied
    return handler

  def get_success_url(self):
    """
      Override get_success_url to redicted user when their post is edited.
    """
    return reverse("blog:view_post", kwargs={"slug": self.object.slug})
  
  def form_valid(self, form):
    """
      Override form_valid function for save every tag typed by user.
      Tags is manager by Django-taggit package.
    """
    tags = form.cleaned_data["tag"]
    self.object = form.save(commit=False)
    self.object.author = self.request.user
    self.object.save()
    
    if tags:
      self.object.tags.add(*tags)
    return HttpResponseRedirect(self.get_success_url())


class PostView(DetailView):
  """
    Post view.

    This Detail view allows users to read a certain post.
  """
  model = models.Post
  template_name = "blog/view_post.html"

  def get_context_data(self, **kwargs):
    """
      Override context_data function for create a few context variables
      for comment section and like/unlike post component.
      New context variables created:
        - comment_form: Contains comment form to attach it in post view template.
        - liked_post: Boolean variable that means if current user like current post.
    """
    context = super().get_context_data(**kwargs)
    context["comment_form"] = forms.CommentForm
    liked_post = False

    if self.request.user.is_authenticated:
      liked_post = self.request.user.likes.filter(slug=self.kwargs["slug"]).exists()
    
    context["liked_post"] = liked_post
    return context


class CreateCommentView(LoginRequiredMixin, CreateView):
  """
    Create comment view.

    This Create view allows users to comment certain post.
  """
  form_class = forms.CommentForm
  
  def get_success_url(self):
    """
      Override get_success_url to redicted user when their commented current post.
    """
    return reverse("blog:view_post", kwargs={"slug": self.object.post.slug})

  def form_valid(self, form):
    """
      Override form_valid function for checking if current post exists and save
      user comment.
    """
    post = get_object_or_404(models.Post, slug=self.kwargs["slug"])
    self.object = form.save(commit=False)
    self.object.post = post
    self.object.author = self.request.user
    self.object.save()
    
    return HttpResponseRedirect(self.get_success_url())


@login_required
def LikePostView(request, slug):
  """
    Like view.

    This view check if current post to like exists and allows users to like it.
  """
  post = get_object_or_404(models.Post, slug=slug)
  post.likes.add(request.user)
  
  return HttpResponseRedirect(
    reverse("blog:view_post", kwargs={"slug": slug})
  )


@login_required
def UnlikePostView(request, slug):
  """
    Unlike view.

    This view check if current post to like exists and allows users to unlike it.
  """
  post = get_object_or_404(models.Post, slug=slug)
  post.likes.remove(request.user)
  
  return HttpResponseRedirect(
    reverse("blog:view_post", kwargs={"slug": slug})
  )


class DeletePostView(LoginRequiredMixin, DeleteView):
  """
    Delete post view.

    This delete view allows user to delete their own post.
  """
  model = models.Post
  success_url = reverse_lazy("blog:home")

  def dispatch(self, request, *args, **kwargs):
    """
      Override dispatch function for security reason.
      Check if current user is accessing to their own post.
      A superuser can delete every user posts.
    """
    handler = super().dispatch(request, *args, **kwargs)
    
    if not (self.request.user == self.object.author or self.request.user.is_superuser):
      raise PermissionDenied
    return handler


class CreateCategoryView(LoginRequiredMixin, CreateView):
  """
    Create category view.

    This create view allows to every user create a category.
  """
  form_class = forms.CategoryForm
  template_name = "blog/create_category.html"
  success_url = reverse_lazy("blog:home")


class AuthorFilterView(ListView):
  """
    Author filter view.

    This list view shows every post filtered by certain author.
  """
  model = models.Post
  template_name = "blog/author_filter.html"

  def get_context_data(self, **kwargs):
    """
      Override context_data function for create a few context variables
      for posts filtering.
      New context variables created:
        - filtered_posts: Contains posts filtered by certain author.
    """
    context = super().get_context_data(**kwargs)
    selected_author = get_object_or_404(models.User, username=self.kwargs["username"])

    context["filtered_posts"] = models.Post.objects.get_published_posts().get_posts_by_author(selected_author)
    context["categories"] = models.Category.objects.all()
    context["authors"] = models.User.objects.filter(blog_posts__isnull=False).distinct("username")
    context["tags"] = models.Tag.objects.all()
    
    return context


class CategoryFilterView(ListView):
  """
    Category filter view.

    This list view shows every post filtered by certain category.
  """
  model = models.Post
  template_name = "blog/category_filter.html"

  def get_context_data(self, **kwargs):
    """
      Override context_data function for create a few context variables
      for posts filtering.
      New context variables created:
        - filtered_posts: Contains posts filtered by certain category.
    """
    context = super().get_context_data(**kwargs)
    selected_category = get_object_or_404(models.Category, slug=self.kwargs["slug"])

    context["filtered_posts"] = models.Post.objects.get_published_posts().get_posts_by_category(selected_category)
    context["categories"] = models.Category.objects.all()
    context["authors"] = models.User.objects.filter(blog_posts__isnull=False).distinct("username")
    context["tags"] = models.Tag.objects.all()
    
    return context


class TagsFilterView(ListView):
  """
    Tags filter view.

    This list view shows every post filtered by certain tag.
  """
  model = models.Post
  template_name = "blog/tags_filter.html"

  def get_context_data(self, **kwargs):
    """
      Override context_data function for create a few context variables
      for posts filtering.
      New context variables created:
        - filtered_posts: Contains posts filtered by certain tag.
    """
    context = super().get_context_data(**kwargs)

    context["filtered_posts"] = models.Post.objects.get_published_posts().get_posts_by_tags([self.kwargs["tag"]])
    context["categories"] = models.Category.objects.all()
    context["authors"] = models.User.objects.filter(blog_posts__isnull=False).distinct("username")
    context["tags"] = models.Tag.objects.all()
    
    return context