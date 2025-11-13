from django import forms
from .models import GroupDocument

class Upload(forms.ModelForm):
  class Meta:
    model = GroupDocument
    fields = ["title", "file"]
