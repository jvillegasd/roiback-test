from taggit.models import Tag
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from .managers import PostManager
from simple_history.models import HistoricalRecords

POST_STATUS = (
  ("draft", "Draft"),
  ("published", "Published")
)

# Create your models here.
class Category(models.Model):
  name = models.CharField(max_length=200, unique=True)
  slug = models.SlugField(max_length=200, unique=True)
  history = HistoricalRecords()

  class Meta:
    ordering = ("name",)
    verbose_name = "category"
    verbose_name_plural = "categories"
  
  def __str__(self):
    return f"<Category: {self.name}>"


class Post(models.Model):
  objects = PostManager()
  title = models.CharField(max_length=300, unique=True)
  slug = models.SlugField(max_length=200, unique=True)
  author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blog_posts")
  content = models.TextField()
  likes = models.ManyToManyField(User, related_name="likes")
  tags = TaggableManager(blank=True)
  category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
  status = models.CharField(choices=POST_STATUS, default="draft", max_length=13)
  publish_date = models.DateTimeField()
  deactivate_date = models.DateTimeField(null=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  history = HistoricalRecords()

  class Meta:
    ordering = ["-created_at"]
  
  def __str__(self):
    return f"<Post: {self.title}>"
  
  @property
  def number_of_likes(self):
    return self.likes.count()


class PostComment(models.Model):
  post = models.ForeignKey(Post, null=True, on_delete=models.CASCADE, related_name="blog_comments")
  author = models.ForeignKey(User, on_delete=models.CASCADE)
  content = models.TextField()
  posted_at = models.DateTimeField(auto_now_add=True)
  history = HistoricalRecords()

  class Meta:
    ordering = ["-posted_at"]
  
  def __str__(self):
    return f"<PostComent: {self.author.username}, {self.post.title}>"