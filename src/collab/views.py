from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import Upload, AddTaskForm
from .models import GroupDocument
from groups.models import Group
from groups.decorators import group_member_required, group_member_required_by_doc

@login_required
@group_member_required
def add_task(resquest):
  form = AddTaskForm()
  group #ajouter
  context = {"form":form}
  if request.method == "POST"
    form = AddTaskForm(request.POST)
    if form.is_valid():
      task = form.save(commit=False)
      task.group = group
  return render(request, "collab/add_task.html", context)

@login_required
@group_member_required
def download_doc(request, id):
  doc = get_object_or_404(GroupDocument, id=id)
  if request.user == doc.user or request.user == doc.group.creator or request.user in doc.group.members.all():
    response = FileResponse(open(doc.file.path, 'rb'))
    return response
  else:
    messages.warning(request, "You are not allowed to download this document.")
    return redirect('user_docs')


@login_required
@group_member_required
def upload(request, id):
  form = Upload()
  group = Group.objects.get(id=id)
  context = {"form":form, "group":group}
  if request.method == "POST":
    form = Upload(request.POST, request.FILES)
    if form.is_valid():
      doc = form.save(commit=False)
      doc.group = group
      doc.user = request.user
      doc.save()
      return redirect("home_group", id=id)
    else:
      messages.info(request, "Form is invalid.")

  return render(request, "collab/upload.html", context)

@login_required
@group_member_required_by_doc
def delete_doc(request, id):
  doc = GroupDocument.objects.get(id=id)
  group_id = doc.group.id
  if request.method == "POST" and (doc.user == request.user or doc.group.creator == request.user) :
    doc.delete()
    messages.success(request, "Document deleted successfully")
    return redirect("home_group", id=group_id)
  else:
    messages.info(request, "You don't have the right to delete this.")
    return redirect("home_group", id=group_id)
