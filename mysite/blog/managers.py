import datetime
from django.db import models
from django.db.models import Q

# Customs Queries Sets
class PostQuerySet(models.query.QuerySet):
  """
    Post query set.

    Custom model QuerySet for Post model. This queryset contains
    some queries usefull for post filtering and which post can be
    considered as 'Published'. So, they can be shown on users feed.
  """

  def get_published_posts(self):
    """
      This function return published posts. It takes into accounts
      posts 'publish date', their 'post status' and their 'deactivate_date'.
    """
    now_date = datetime.datetime.now()
    posts = self.filter(
      Q(publish_date__lte=now_date) &
      Q(status="published") &
      (Q(deactivate_date=None) | Q(deactivate_date__gte=now_date))
    )

    return posts
  
  def get_posts_by_category(self, category):
    """
      This functions returns every posts filtered by a category.
    """
    return self.filter(category=category)
  
  def get_posts_by_author(self, author):
    """
      This functions returns every posts filtered by an author.
    """
    return self.filter(author=author)
  
  def get_posts_by_tags(self, tags):
    """
      This functions returns every posts filtered by a tag.
    """
    return self.filter(tags__name__in=tags)


# Custom Managers
class PostManager(models.Manager):
  """
    Post manager.

    This model manager is used to modify default Post model manager for
    use defined custom QuerySet class methods.
  """

  def get_queryset(self):
    return PostQuerySet(self.model, using=self._db)
  
  def get_published_posts(self):
    return self.get_queryset().get_published_posts()

  def get_posts_by_category(self, category):
    return self.get_queryset().get_posts_by_category(category)

  def get_posts_by_author(self, author):
    return self.get_queryset().get_posts_by_author(author)

  def get_posts_by_tags(self, tags):
    return self.get_queryset().get_posts_by_tags(tags)