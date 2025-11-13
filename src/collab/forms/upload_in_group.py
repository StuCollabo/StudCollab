from django import forms
from fichiers.models import GroupDocument

class UploadInGroupForm(forms.ModelForm):
  class Meta:
    model = GroupDocument
    fields = ["title", "file"]
    labels = {
      "title":"Doc name"
    }
