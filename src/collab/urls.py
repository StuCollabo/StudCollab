from django.urls import path
from . import views

urlpatterns = [
    # Vue principale pour téléverser un document
    path('', views.televerser, name='depot'),

    # Vue pour lister les documents
    path('documents/', views.document_list, name='documents'),

    # URLs AJAX pour le filtrage dynamique (AVEC niveau maintenant)
    path('ajax/filieres/<int:faculte_id>/<int:niveau_id>/<str:annee_academique>/',
         views.obtenir_filieres, name='obtenir_filieres'),

    path('ajax/matieres/<int:filiere_id>/<int:niveau_id>/<str:annee_academique>/',
         views.obtenir_matieres, name='obtenir_matieres'),
]
