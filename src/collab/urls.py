from django.urls import path
from . import views

urlpatterns = [
    path('upload/<int:id>', views.upload, name='upload'),
]
