from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User
from django import forms

class SignUpForm(UserCreationForm):
  class Meta:
    model = User
    fields = ["username", "email", "password1", "password2"]

  def clean_username(self):
    username = self.cleaned_data["username"]
    return username.lower()


class ModifyUserInfoForm(forms.ModelForm):
  class Meta:
    model = User
    fields = ["username", "email"]

  def clean_username(self):
    username = self.cleaned_data.get("username")
    if username:
      return username.lower()
    return username


from django.contrib.auth.forms import AuthenticationForm

class LowercaseAuthenticationForm(AuthenticationForm):
  def clean_username(self):
    username = self.cleaned_data.get('username')
    if username:
      return username.lower()
    return username

