from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager

POST_STATUS = (
  ("draft", "Draft"),
  ("published", "Published")
)

TRANSACTIONS_TYPES = (
  ("post_creation", "Post_creation"),
  ("post_deletion", "Post_deletion"),
  ("Post_modification", "Post_modification"),
  ("post_comment", "Post_comment"),
  ("post_like", "Post_like"),
  ("user_creation", "User_creation")
)

# Create your models here.
class Category(models.Model):
  name = models.CharField(max_length=200, unique=True)
  slug = models.SlugField(max_length=200, unique=True)

  class Meta:
    ordering = ("name",)
    verbose_name = "category"
    verbose_name_plural = "categories"
  
  def __str__(self):
    return f"<Category: {self.name}>"


class Post(models.Model):
  title = models.CharField(max_length=300, unique=True)
  slug = models.SlugField(max_length=200, unique=True)
  author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blog_posts")
  content = models.TextField()
  likes = models.ManyToManyField(User, related_name="likes")
  tags = TaggableManager()
  category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
  status = models.CharField(choices=POST_STATUS, default="draft", max_length=13)
  publish_date = models.DateTimeField()
  deactivate_date = models.DateTimeField(null=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    ordering = ["-created_at"]
  
  def __str__(self):
    return f"<Post: {self.title}>"
  
  @property
  def number_of_comments(self):
    return PostComent.objects.filter(post=self).count()
  
  @property
  def number_of_likes(self):
    return self.likes.count()


class PostComment(models.Model):
  post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="blog_comments")
  author = models.ForeignKey(User, on_delete=models.CASCADE)
  content = models.TextField()
  posted_at = models.DateTimeField(auto_now_add=True)

  class Meta:
    ordering = ["-posted_at"]
  
  def __str__(self):
    return f"<PostComent: {self.author.username}, {self.post.title}>"


class Transaction(models.Model):
  author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_transactions")
  transaction_type = models.CharField(choices=TRANSACTIONS_TYPES, max_length=60)
  created_at = models.DateTimeField(auto_now_add=True)

  class Meta:
    ordering = ["-created_at"]

  def __str__(self):
    return f"<Transaction: {self.author.username}, {self.transaction_type}>"