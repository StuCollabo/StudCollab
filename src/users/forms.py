from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User
from django import forms

class SignUpForm(UserCreationForm):
  class Meta:
    model = User
    fields = ["username", "email", "password1", "password2"]

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['username'].widget.attrs.update({
      'placeholder': 'Username'
    })
    self.fields['email'].widget.attrs.update({
      'placeholder': 'Email address'
    })
    self.fields['password1'].widget.attrs.update({
      'placeholder': 'Password'
    })
    self.fields['password2'].widget.attrs.update({
      'placeholder': 'Confirm password'
    })

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
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['username'].widget.attrs.update({
      'placeholder': 'Username'
    })
    self.fields['password'].widget.attrs.update({
      'placeholder': 'Password'
    })

  def clean_username(self):
    username = self.cleaned_data.get('username')
    if username:
      return username.lower()
    return username
