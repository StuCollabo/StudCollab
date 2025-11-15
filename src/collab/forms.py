from django import forms
from .models import GroupDocument, Task
from users.models import User

class Upload(forms.ModelForm):
  class Meta:
    model = GroupDocument
    fields = ["title", "file"]
"""
class AddTaskForm(forms.ModelForm):
  class Meta:
    models = Task
    fields = ["title", "assigned_to"]
"""

class AddTaskForm(forms.ModelForm):
  class Meta:
    model = Task
    fields = ["title", "assigned_to"]

  def __init__(self, *args, **kwargs):
    group = kwargs.pop("group", None)
    super().__init__(*args, **kwargs)

    if group:
      # Les utilisateurs autorisés = créateur + membres
      allowed_users = group.members.all(
      ) | User.objects.filter(id=group.creator.id)
      self.fields["assigned_to"].queryset = allowed_users
