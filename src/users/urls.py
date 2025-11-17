from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
  path('', views.show_dashboard, name="dashboard"),
  path("signin_signup/", views.signin_signup,
    name="signin_signup"),
  path("modify/profile/", views.modify_user_info, name="modify_profile"),
  path("my-docs/", views.get_user_docs, name="user_docs"),
  path("delete-account/", views.delete_user,
    name="delete_user"),
  path("notifs/", views.show_notifs, name="notifs"),
  path("notifs/delete/<int:notif_id>/",
    views.delete_notif, name="delete_notif"),

  
  #Formulaire mot de passe oublié
  path("reset-password/",
    auth_views.PasswordResetView.as_view(),
    name="reset_password"),

  #Comfirmation page after sent
  path("password-reset-done/",
    auth_views.PasswordResetDoneView.as_view(),
    name="password_reset_done"),

  #Clicked link in email with token
  path('reset/<uidb64>/<token>/', 
    auth_views.PasswordResetConfirmView.as_view(), 
    name='password_reset_confirm'),

  #Final confirmation
  path('reset/done/', 
    auth_views.PasswordResetCompleteView.as_view(), 
    name='password_reset_complete'),

]

