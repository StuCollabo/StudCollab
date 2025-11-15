from django.urls import path
from . import views

urlpatterns = [
  path('upload/<int:id>/', views.upload, name='upload'),
  path('delete/<int:id>/', views.delete_doc, name="delete_doc"),
  path('download/<int:id>/', views.download_doc, name="download_doc"),
  path('<int:id>/add-task/', views.add_task, name="add_task"),
 
]
