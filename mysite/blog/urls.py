from . import views
from . import forms
from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("sign_in/", auth_views.LoginView.as_view(
        template_name="blog/sign_in.html",
        authentication_form=forms.SigninForm
        ), name="sign_in"),
    path("sign_up/", views.SignupView.as_view(), name="sign_up"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("home/", views.HomeView.as_view(), name="home"),
    path("create_post/", views.CreatePostView.as_view(), name="create_post"),
    path("create_category/", views.CreateCategoryView.as_view(), name="create_category"),
    path("post/<slug:slug>/", views.PostView.as_view(), name="view_post"),
    path("post/<slug:slug>/add_comment/", views.CreateCommentView.as_view(), name="add_comment"),
    path("post/<slug:slug>/like/", views.LikePostView, name="like_post"),
    path("post/<slug:slug>/unlike/", views.UnlikePostView, name="unlike_post"),
    path("post/<slug:slug>/edit/", views.EditPostView.as_view(), name="edit_post"),
    path("post/<slug:slug>/delete/", views.DeletePostView, name="delete_post"),
    path("filter/author/<str:username>/", views.AuthorFilterView.as_view(), name="author_filter"),
    path("filter/category/<slug:slug>/", views.CategoryFilterView.as_view(), name="category_filter"),
    path("filter/tags/<str:tag>/", views.TagsFilterView.as_view(), name="tags_filter")
]