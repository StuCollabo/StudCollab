from django import forms
from .models import Group

class CreateGroupForm(forms.ModelForm):
  class Meta:
    model = Group
    fields = ["name"]
    widgets = {
      'name' : forms.TextInput(attrs={
           'placeholder': 'Enter the name of the group'
      })
    }


class JoinGroupForm(forms.Form):
  invit_code = forms.CharField(
    max_length=36,
    label="Invitation code"
  )


class RenameGroupForm(forms.ModelForm):
  class Meta:
    model = Group
    fields = ["name"]
    widgets = {
      'name' : forms.TextInput(attrs={
           'placeholder': 'Enter the name of the group'
      })
    }
