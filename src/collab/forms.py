from django import forms
from .models import GroupDocument, Task
from users.models import User
from groups.models import SubGroup


class ModifyDocForm(forms.ModelForm):
  class Meta:
    model = GroupDocument
    fields = ["title", "is_visible"]

class Upload(forms.ModelForm):
  class Meta:
    model = GroupDocument
    fields = ["title", "file", "is_visible"]


class AddTaskForm(forms.ModelForm):
  class Meta:
    model = Task
    fields = ["title", "assigned_to", "subgroup"]


  def __init__(self, *args, **kwargs):
    group = kwargs.pop("group", None)
    print("kwargs = ", kwargs)
    print("Group = ", group)
    super().__init__(*args, **kwargs)

    if group:
      # Les utilisateurs autorisés = créateur + membres
      allowed_users = (group.members.all(
      ) | User.objects.filter(id=group.creator.id)).distinct()
      self.fields["assigned_to"].queryset = allowed_users

      # Les sous-groupesvautorisés 
      allowed_subgroups = SubGroup.objects.filter(group=group)
      self.fields["subgroup"].queryset = allowed_subgroups
