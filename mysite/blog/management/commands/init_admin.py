import os
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User


class Command(BaseCommand):
  help = "Create super user using env credentials"

  def handle(self, *args, **options):
    admin_username = os.environ.get("ADMIN_USERNAME")
    admin_password = os.environ.get("ADMIN_PASSWORD")
    admin_email = os.environ.get("ADMIN_EMAIL")

    admin_exists = User.objects.filter(username=admin_username).exists()
    if not admin_exists:
      admin_user = User.objects.create_superuser(
        username=admin_username, 
        password=admin_password, 
        email=admin_email
      )
      admin_user.save()
      self.stdout.write(f"Admin user {admin_username} created successfully!")
    else:
      self.stdout.write(f"Admin user {admin_username} already exists, skipping..")