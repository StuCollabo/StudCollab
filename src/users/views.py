from django.shortcuts import render, redirect, get_object_or_404
from .forms import SignUpForm, ModifyUserInfoForm, LowercaseAuthenticationForm
from django.contrib.auth import authenticate, login, update_session_auth_hash, logout
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from collab.models import GroupDocument, Notification
from django.http import HttpResponseRedirect
from django.urls import reverse

@login_required
def delete_notif(request, notif_id):
  notif = get_object_or_404(Notification, id=notif_id)
  if request.user == notif.user:
    if request.method == "POST":
      notif.delete()
      messages.success(request, "Notification deleted successfully.")
      return redirect("notifs")
  else:
    messages.warning(request, "You don't have the right to delete this ressource.")
    return redirect("notifs")

@login_required
def show_notifs(request):
  notifs = Notification.objects.filter(user=request.user).prefetch_related('triggered_by', 'task__group')
  context = {"notifs":notifs}

  return render(request, "users/notifications.html", context)


@login_required
def delete_user(request):
  if request.method == "POST":
    user = request.user
    logout(request)
    user.delete()
    messages.success(request, "Account deleted successfully.")
    return HttpResponseRedirect(reverse('home'))
  return  HttpResponseRedirect(reverse('dashboard'))

@login_required
def modify_user_info(request):
  info_form = ModifyUserInfoForm(instance=request.user)
  password_form = PasswordChangeForm(request.user)
  context ={"info_form":info_form,
      "password_form":password_form}

  if request.method == "POST":

    if "submit_personal" in request.POST:
      info_form = ModifyUserInfoForm(request.POST, instance=request.user)
      if info_form.is_valid():
        info_form.save()
        messages.success(request, "Account updated successfully")
        return redirect("dashboard")
      else:
        messages.info(request, "Something went wrong (bis)")

    elif "submit_password" in request.POST:
      password_form = PasswordChangeForm(request.user,
          request.POST)
      if password_form.is_valid():
        user = password_form.save()
        update_session_auth_hash(request, user)
        messages.success(request, "Mot de passe modifié avec succès !")
      else:
        messages.info(request, "Something went wrong")
  return render(request, "users/modify_user.html", context)


@login_required
def show_dashboard(request):
  if request.user.username.endswith("s"):
    dashboard_title = f"{request.user.username}' space"
  else:
    dashboard_title = f"{request.user.username}'s space"
  count_docs = GroupDocument.objects.filter(user=request.user).count()
  context = {"user":request.user,
    "dashboard_title":dashboard_title,
    "count_docs":count_docs}
  return render(request, "users/dashboard.html", context)


@login_required
def get_user_docs(request):
  docs = GroupDocument.objects.filter(user=request.user)
  context = {"docs":docs}
  return render(request, "users/user_docs.html", context)


def signin_signup(request):
  if request.user.is_authenticated:
    messages.info(request, "You're already authenticated")
    return redirect("home")

  signin_form = AuthenticationForm()
  signup_form = SignUpForm()
  context = {"signin_form":signin_form,
    "signup_form":signup_form}

  if request.method == "POST":

    if "signup_submit" in request.POST:
      signup_form = SignUpForm(request.POST)
      if signup_form.is_valid():
        user = signup_form.save()
        login(request, user)
        next_url = request.GET.get("next") or '/'
        return redirect(next_url)

    elif "signin_submit" in request.POST:
      signin_form = LowercaseAuthenticationForm(request, data=request.POST)
      if signin_form.is_valid():
        login(request, signin_form.get_user())
        next_url = request.GET.get("next") or '/'
        return redirect(next_url)
      else:
        if "__all__" in signin_form.errors:
          print(signin_form.errors)
          messages.info(request, "You messed up.")

  return render(request, "users/signin_signup.html", context)
