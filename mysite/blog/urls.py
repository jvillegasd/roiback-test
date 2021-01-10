from . import views
from . import forms
from django.conf.urls import url
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r"^$", views.IndexView.as_view(), name="index"),
    url(r"^sign_in/$", auth_views.LoginView.as_view(
        template_name="blog/sign_in.html",
        authentication_form=forms.SigninForm
        ), name="sign_in"),
    url(r"^sign_up/$", views.SignupView.as_view(), name="sign_up"),
    url(r"^logout/$", auth_views.LogoutView.as_view(), name="logout"),
    url(r"^home/$", views.HomeView.as_view(), name="home")
]