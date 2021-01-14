import datetime
from django.db import models
from django.db.models import Q

# Customs Queries Sets
class PostQuerySet(models.query.QuerySet):

  def get_published_posts(self):
    now_date = datetime.datetime.now()
    posts = self.filter(
      Q(publish_date__lte=now_date) &
      Q(status="published") &
      (Q(deactivate_date=None) | Q(deactivate_date__gte=now_date))
    )

    return posts
  
  def get_posts_by_category(self, category):
    return self.filter(category=category)
  
  def get_posts_by_author(self, author):
    return self.filter(author=author)
  
  def get_posts_by_tags(self, tags):
    return self.filter(tags__name__in=tags)


# Custom Managers
class PostManager(models.Manager):

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