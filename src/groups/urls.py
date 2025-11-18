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

  #About Subgroups
  path("<int:id>/subgroups/", views.list_subgroups, name="list_subgroups"),
  path("<int:id>/subgroups/create/", views.create_subgroup, name="create_subgroup"),
  path("<int:id>/subgroups/join/", views.join_subgroup,
    name="join_subgroup"),
  path("<int:id>/subgroups/<int:sg_id>/",
    views.get_home_subgroup, name="home_subgroup"),
  path("<int:id>/subgroups/delete/<int:sg_id>/",
    views.delete_subgroup, name="delete_subgroup"),
  path("<int:id>/subgroups/rename/<int:sg_id>/",
    views.rename_subgroup, name="rename_subgroup"),

]
