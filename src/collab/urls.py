from django.urls import path
from . import views

urlpatterns = [
  path('upload/<int:id>/', views.upload, name='upload'),
  path('delete/<int:id>/', views.delete_doc, name="delete_doc"),
  path('download/<int:id>/', views.download_doc, name="download_doc"),
  path('<int:id>/add-task/', views.add_task, name="add_task"),
  path('tasks/<int:task_id>/toggle/', views.toggle_task, name='toggle_task'),
  path('<int:id>/tasks/undone/',
    views.see_undone_tasks,
    name="undone_tasks"),
  path('tasks/<int:task_id>/wake/',
    views.wake_them, name="wake_them"),
  path("<int:id>/logs/", views.show_logs,
    name="show_logs"),
]
