from functools import wraps
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Group 
from collab.models import GroupDocument
from collab.models import Task

def task_member_required(view_func):
  @wraps(view_func)
  def _wrapped_view(request, task_id, *args, **kwargs):
    task = get_object_or_404(Task, id=task_id)
    group = task.group

    if request.user == group.creator or request.user in group.members.all():
      return view_func(request, task_id, *args, **kwargs)

    messages.warning(request, "You are not allowed to manage tasks from this group.")
    return redirect("list_groups")

  return _wrapped_view


def group_member_required(view_func):
    """
    Vérifie que l'utilisateur connecté est membre ou créateur du groupe.
    Le décorateur suppose que la vue a un paramètre 'id' pour l'ID du groupe.
    """
    @wraps(view_func)
    def _wrapped_view(request, id, *args, **kwargs):
        group = get_object_or_404(Group, id=id)
        if request.user == group.creator or request.user in group.members.all():
            # OK, l'utilisateur a le droit, on continue
            return view_func(request, id, *args, **kwargs)
        else:
            # Sinon, message d'erreur et redirection
            messages.warning(request, "You are not a member of this group.")
            return redirect("dashboard")
    return _wrapped_view



def group_member_required_by_doc(view_func):

    @wraps(view_func)
    def _wrapped_view(request, id, *args, **kwargs):  # id = doc_id
        doc = get_object_or_404(GroupDocument, id=id)
        group = doc.group
        if request.user == group.creator or request.user in group.members.all():
            return view_func(request, id, *args, **kwargs)
        else:
            messages.warning(request, "You are not a member of this group.")
            return redirect("dashboard")
    return _wrapped_view
