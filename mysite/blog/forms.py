import datetime
from .models import POST_STATUS, Post, Category, PostComment
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django import forms
from taggit.forms import TagWidget, TagField

class SigninForm(AuthenticationForm):
  
  def __init__(self, *args, **kwargs):
    super(SigninForm, self).__init__(*args, **kwargs)

  username = forms.CharField(widget=forms.TextInput(
    attrs={
      "class": "form-control",
      "placeholder": "Type your username",
      "id": "username",
      "required": "required",
      "autofocus": "autofocus"
    }
  ))
  password = forms.CharField(widget=forms.PasswordInput(
    attrs={
      "class": "form-control",
      "placeholder": "Type your password",
      "id": "password",
      "required": "required"
    }
  ))


class SignupForm(UserCreationForm):

  def __init__(self, *args, **kwargs):
    super(SignupForm, self).__init__(*args, **kwargs)
  
  username = forms.CharField(widget=forms.TextInput(
    attrs={
      "class": "form-control",
      "placeholder": "Type your username",
      "id": "username",
      "required": "required",
      "autofocus": "autofocus"
    }
  ))
  password1 = forms.CharField(widget=forms.PasswordInput(
    attrs={
      "class": "form-control",
      "placeholder": "Type your password",
      "id": "password1",
      "required": "required"
    }
  ))
  password2 = forms.CharField(widget=forms.PasswordInput(
    attrs={
      "class": "form-control",
      "placeholder": "Confirm your password",
      "id": "password2",
      "required": "required"
    }
  ))
  
  class Meta:
    model = User
    fields = ("username", "password1", "password2")


class PostForm(forms.ModelForm):

  title = forms.CharField(widget=forms.TextInput(
    attrs={
      "class": "form-control",
      "required": "required",
      "placeholder": "New post title"
    }
  ))
  slug = forms.CharField(widget=forms.TextInput(
    attrs={
      "class": "form-control",
      "required": "required",
      "placeholder": "New post slug"
    }
  ))
  category = forms.ModelChoiceField(widget=forms.Select(
    attrs={
      "class": "form-control",
    }),
    queryset=Category.objects.all(), 
    empty_label="(Nothing)",
    required=False
  )
  tag = TagField(widget=TagWidget(
    attrs={
      "class": "form-control",
      "placeholder": "Type tags separate with space"
    }),
    required=False
  )
  content = forms.CharField(widget=forms.Textarea(
    attrs={
      "class": "form-control",
      "required": "required",
      "style": "resize: none;"
    }
  ))
  status = forms.ChoiceField(widget=forms.Select(
    attrs={
      "class": "form-control",
    }),
    choices=POST_STATUS
  )
  publish_date = forms.DateTimeField(widget=forms.DateTimeInput(
    format="%d/%m/%Y",
    attrs={
      "class": "form-control datepicker",
      "autocomplete":"off"
    }),
    input_formats=["%d/%m/%Y"]
  )
  deactivate_date = forms.DateTimeField(widget=forms.DateTimeInput(
    format="%d/%m/%Y",
    attrs={
      "class": "form-control datepicker",
      "autocomplete":"off"
    }),
    input_formats=["%d/%m/%Y"],
    required=False
  )

  class Meta:
    model = Post
    fields = ("title", "slug", "category", "tag", "content", "status", "publish_date", "deactivate_date")
    exclude = ["author"]


class CategoryForm(forms.ModelForm):

  name = forms.CharField(widget=forms.TextInput(
    attrs={
      "class": "form-control",
      "required": "required",
      "placeholder": "New category name"
    }
  ))
  slug = forms.CharField(widget=forms.TextInput(
    attrs={
      "class": "form-control",
      "required": "required",
      "placeholder": "New category slug"
    }
  ))

  class Meta:
    model = Category
    fields = ("name", "slug")


class CommentForm(forms.ModelForm):

  content = forms.CharField(widget=forms.Textarea(
    attrs={
      "class": "form-control",
      "required": "required",
      "style": "resize: none; width: 100%; overflow-y: scroll; display: inline-block; height: 100px;"
    }
  ))

  class Meta:
    model = PostComment
    fields = ("content",)