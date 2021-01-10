from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django import forms

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