from django.shortcuts import render, get_object_or_404, redirect
from .forms import JoinGroupForm, CreateGroupForm, RenameGroupForm
from .models import Group
import uuid
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from collab.models import GroupDocument
from .decorators import group_member_required

@login_required
def rename_group(request, id):
  group = Group.objects.get(id=id)
  form = RenameGroupForm(instance=group)
  old_name = Group.objects.get(id=id).name
  context = {"old_name":old_name,
    "form":form, "group":group}
  if request.method == "POST":
    form = RenameGroupForm(request.POST, instance=group)
    if form.is_valid():
      group = form.save()
      messages.success(request,
        f"Group {old_name} was successfully renamed to {group.name}.")
      return redirect("list_groups")

  return render(request, "groups/rename_group.html", context)


@login_required
def delete_group(request, id):
  group = Group.objects.get(id=id)
  is_creator = group.creator == request.user
  if is_creator:
    if request.method == "POST":
      group.delete()
      messages.success(request, "Group deleted successfully.")
      return redirect("list_groups")
  else:
    messages.info(request, "You're not allowed to do this.")
    return redirect("list_groups")


@login_required
def list_groups(request):
  groups = (Group.objects.filter(members=request.user)
    | Group.objects.filter(creator=request.user)
    ).distinct()
  context = {"groups":groups}

  return render(request, "groups/list_groups.html", context)

@login_required
@group_member_required
def get_home_group(request, id):
  group = get_object_or_404(Group, id=id)
  documents = GroupDocument.objects.filter(group=group)
  context = {"group":group, "documents":documents}
  
  return render(request, "groups/home_group.html", context)

@login_required
def join_group(request):
  form = JoinGroupForm()
  context = {"form":form}

  if request.method == "POST":
    form = JoinGroupForm(request.POST)
    if form.is_valid():
      invit_code_str = form.cleaned_data["invit_code"].strip()
      print(invit_code_str)
#      try:
      invit_code_uuid = uuid.UUID(invit_code_str)
      group = Group.objects.get(invit_code=invit_code_uuid)
      if request.user != group.creator and request.user not in group.members.all():
        group.members.add(request.user)
        return redirect("home_group", id=group.id)
      else:
        url = reverse("home_group", kwargs={"id":group.id})
        messages.info(request, f"You already belong to<a href={url}>{group.name}</a>.")
#      except (Group.DoesNotExist, ValueError):
#      form.add_error('invit_code', 'Invalid Code.')

  return render(request, "groups/join_group.html", context)

@login_required
def create_group(request):
  form = CreateGroupForm()
  context = {"form":form}
  if request.method == "POST":
    form = CreateGroupForm(request.POST)
    if form.is_valid():
      group = form.save(commit=False)
      group.creator = request.user
      group.save()
      return redirect("home_group", id=group.id)

  return render(request, "groups/create_group.html", context)
