from django.shortcuts import render
from django.db.models import Q
from fichiers.models import PublicDocument, Faculte, Filiere


def accueil(request):
  user = request.user
  filiere = Filiere.objects.all().count()
  faculte = Faculte.objects.all().count()
  context = {'filiere':filiere,
    'user': user, 'faculte':faculte}
  return render(request, 'base/accueil.html', context)

def aide(request):
  return render(request, "base/aide.html")

def apropos(request):
  return render(request, "base/apropos.html")

def documents(request):
  # Récupère les 10 derniers documents ajoutées
  documents_recents = PublicDocument.objects.filter(pk__isnull=False
    ).order_by("-created_at")[:10]
  return render(request, 'base/documents.html', {
      'documents_recents': documents_recents
  })



def recherche(request):
    # Récupérer les paramètres du formulaire
    query = request.GET.get('titre', '')  # correspond au champ HTML
    annee_academique = request.GET.get('annee_academique')
    resultats = PublicDocument.objects.all()

    # Recherche texte libre
    if query:
        resultats = resultats.filter(
            Q(titre__icontains=query) |
            Q(matiere__nom__icontains=query) |
            Q(type__type__icontains=query) |
            Q(matiere__classe__niveau__niveau__icontains=query) |
            Q(matiere__classe__faculte__nom__icontains=query) |
            Q(matiere__classe__filiere__nom__icontains=query) |
            Q(matiere__classe__annee_academique__icontains=query)

        ).distinct()

    # Filtres numériques
    if annee_academique:
        resultats = resultats.filter(matiere__classe__annee_academique__gte=annee_academique).distinct()

    return render(request, 'base/resultats.html', {
        'query': query,
        'resultats': resultats
    })

