from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django import forms

class SignUpForm(UserCreationForm):
  class Meta:
    model = CustomUser
    fields = ["username", "email", "password1", "password2"]

class ModifyUserInfoForm(forms.ModelForm):
  class Meta:
    model = CustomUser
    fields = ["username", "email"]

