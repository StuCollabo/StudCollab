from django import forms
from .models import Group, SubGroup
from users.models import User


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


class CreateSubGroupForm(forms.ModelForm):
  class Meta:
    model = SubGroup
    fields = ["name", "members", "head"]
    widgets = {
      'name' : forms.TextInput(attrs={
           'placeholder': 'Enter the name of the subgroup'
      })
    }
  def __init__(self, *args, **kwargs):
    group = kwargs.pop("group", None)
    print("kwargs = ", kwargs)
    print("Group = " , group)
    super().__init__(*args, **kwargs)

    if group:
      # Les utilisateurs autorisés = créateur + membres
      allowed_users = (group.members.all(
      ) | User.objects.filter(id=group.creator.id)).distinct()
      self.fields["members"].queryset = allowed_users
      self.fields["head"].queryset = allowed_users


class JoinSubGroupForm(forms.Form):
  invit_code = forms.CharField(
    max_length=36,
    label="Invitation code"
  )


class RenameSubGroupForm(forms.ModelForm):
  class Meta:
    model = SubGroup
    fields = ["name"]
    widgets = {
      'name' : forms.TextInput(attrs={
           'placeholder': 'Enter the name of the subgroup'
      })
    }
