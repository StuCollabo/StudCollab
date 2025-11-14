from django.urls import path
from . import views
urlpatterns = [
  path('', views.show_dashboard, name="dashboard"),
  path("signin_signup/", views.signin_signup,
    name="signin_signup"),
  path("modify/profile/", views.modify_user_info, name="modify_profile"),
  path("my-docs/", views.get_user_docs, name="user_docs"),

]

