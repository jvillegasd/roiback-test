from . import views
from django.conf.urls import url

urlpatterns = [
    url("", views.IndexView.as_view(), name="index"),
]