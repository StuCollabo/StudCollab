from django.urls import path
from . import views

urlpatterns = [
  path("join/", views.join_group, name="join_group"),
  path("create/", views.create_group, name="create_group"),
  path("<int:id>/", views.get_home_group,
    name="home_group"),
  path("", views.list_groups, name="list_groups"),
  path("delete/<int:id>/", views.delete_group, name="delete_group"),
  path("rename/<int:id>/", views.rename_group, name="rename_group"),


]
