from django.urls import path
from . import views

urlpatterns = [
    path('', views.accueil, name="accueil"),
    path('aide/', views.aide, name="aide"),
    path('apropos/', views.apropos, name="apropos"),
    path('documents/', views.documents, name="documents"),
    path('recherche/', views.recherche, name="recherche"),
]
