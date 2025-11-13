from django.shortcuts import render, redirect
from .forms import SignUpForm, ModifyUserInfoForm
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm


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

def show_dashboard(request):
  if request.user.username.endswith("s"):
    dashboard_title = f"{request.user.username}' space"
  else:
    dashboard_title = f"{request.user.username}'s space"

  context = {"user":request.user,
    "dashboard_title":dashboard_title}
  return render(request, "users/dashboard.html", context)

def show_profile(request):
  return render(request, "users/profile.html")

def signin_signup(request):
  if request.user.is_authenticated:
    return redirect("accueil")

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
      signin_form = AuthenticationForm(request, data=request.POST)
      if signin_form.is_valid():
        login(request, signin_form.get_user())
        next_url = request.GET.get("next") or '/'
        return redirect(next_url)
      else:
        if "__all__" in signin_form.errors:
          messages.info(request, settings.MESSAGE_SIGNIN)

  return render(request, "users/signin_signup.html", context)
