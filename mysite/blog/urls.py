from . import views
from . import forms
from django.conf.urls import url
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r"^$", views.IndexView.as_view(), name="index"),
    url(r"^sign_in/$", auth_views.LoginView.as_view(
        template_name="blog/sign_in.html",
        authentication_form=forms.SigninForm
        ), name="sign_in")
]