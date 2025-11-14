from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import Upload
from .models import GroupDocument
from groups.models import Group

@login_required
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
