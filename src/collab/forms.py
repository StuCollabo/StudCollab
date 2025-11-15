from django import forms
from .models import GroupDocument, Task

class Upload(forms.ModelForm):
  class Meta:
    model = GroupDocument
    fields = ["title", "file"]

class AddTaskForm(forms.ModelForm):
  class Meta:
    models = Task
    fields = ["title", "assigned_to"]

