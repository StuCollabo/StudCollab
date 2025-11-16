from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import Upload, AddTaskForm
from .models import GroupDocument, Task, Notification
from groups.models import Group
from groups.decorators import group_member_required, group_member_required_by_doc, task_member_required


@login_required
@task_member_required
def wake_them(request, task_id):
  task = get_object_or_404(Task, id=task_id)
  if request.method == "POST":
    notif, created = Notification.objects.get_or_create(
      task=task, user=task.assigned_to)
    notif.triggered_by.add(request.user)
    messages.success(request, f"The reminder has been sent to {task.assigned_to.username}.")
    return redirect("undone_tasks", id=task.group.id)

@login_required
@group_member_required
def see_undone_tasks(request, id):
  group = get_object_or_404(Group, id=id)
  tasks = Task.objects.filter(group=group).filter(completed=False)
  context = {"tasks":tasks, "group":group}
  return render(request, "collab/undone_tasks.html", context)


@login_required
@task_member_required
def toggle_task(request, task_id):
  task = get_object_or_404(Task, id=task_id)

  # Seul l'utilisateur assigné peut modifier la tâche
  if request.user != task.assigned_to:
    messages.warning(request, "Only the assigned user can update this task.")
    return redirect("home_group", id=task.group.id)

  if request.method == "POST":
    task.completed = "completed" in request.POST
    task.save()

  return redirect("home_group", id=task.group.id)


@login_required
@group_member_required
def add_task(request, id):
  group = get_object_or_404(Group, id=id)
  form = AddTaskForm(group=group)
  group = get_object_or_404(Group, id=id)
  context = {"form":form, "group":group}
  if request.method == "POST":
    form = AddTaskForm(request.POST, group=group)
    if form.is_valid():
      task = form.save(commit=False)
      task.group = group
      task.save()
      messages.success(request, "Task added successfully.")
      return redirect("home_group", id=id)
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
    doc.file.delete(save=False)
    doc.delete()
    messages.success(request, "Document deleted successfully")
    return redirect("home_group", id=group_id)
  else:
    messages.info(request, "You don't have the right to delete this.")
    return redirect("home_group", id=group_id)
