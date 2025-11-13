from django.contrib.auth.forms import UserCreationForm
from .models import User
from django import forms

class SignUpForm(UserCreationForm):
  class Meta:
    model = User
    fields = ["username", "email", "password1", "password2"]

class ModifyUserInfoForm(forms.ModelForm):
  class Meta:
    model = User
    fields = ["username", "email"]

