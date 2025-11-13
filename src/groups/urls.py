from django.urls import path
from . import views
from depot.views import upload_in_group
urlpatterns = [
  path("join/", views.join_group, name="join_group"),
  path("create/", views.create_group, name="create_group"),
  path("home_group/<int:id>/", views.home_group,
    name="home_group"),
  path("", views.list_groups, name="list_groups"),
  path("home_group/<int:id>/upload/", upload_in_group, name="upload_in_group"),
]
