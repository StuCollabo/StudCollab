from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.conf import settings
from fichiers.models import Filiere, Matiere, PublicDocument, Classe, Niveau
from depot.forms import TeleverserForm, UploadInGroupForm
from fichiers.models import GroupDocument
from groups.models import Group


@login_required
def upload_in_group(request, id):
  form = UploadInGroupForm()
  group = Group.objects.get(id=id)
  context = {"form":form, "group":group}
  if request.method == "POST":
    form = UploadInGroupForm(request.POST, request.FILES)
    if form.is_valid():
      doc = form.save(commit=False)
      doc.group = group
      doc.user = request.user
      doc.save()
      return redirect("home_group", id=id)
    else:
      messages.info(request, "Form is invalid.")

  return render(request, "groups/upload_in_group.html", context)


def televerser(request):
    user = request.user
    if request.method == "POST":
        form = TeleverserForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save()
            messages.success(request, f'Document "{document.titre}" téléversé avec succès!')
            return redirect('documents')
        else:
            messages.error(request, 'Veuillez corriger les erreurs ci-dessous.')
    else:
        form = TeleverserForm()

    return render(request, 'depot/depot.html',
      {'form': form, 'user':user})

@require_http_methods(["GET"])
def obtenir_filieres(request, faculte_id, niveau_id, annee_academique):
    """Récupère les filières pour une faculté, un niveau et une année donnés"""
    try:
        filieres = list(Filiere.objects.filter(
            faculte_id=faculte_id,
            classe__niveau_id=niveau_id,
            classe__annee_academique=annee_academique
        ).distinct().values('id', 'nom'))

        print(f"Debug - Faculté: {faculte_id}, Niveau: {niveau_id}, Année: {annee_academique}")
        print(f"Debug - Filières trouvées: {filieres}")

        return JsonResponse(filieres, safe=False)
    except Exception as e:
        print(f"Erreur dans obtenir_filieres: {e}")
        return JsonResponse({'error': 'Erreur lors de la récupération des filières'}, status=500)

@require_http_methods(["GET"])
def obtenir_matieres(request, filiere_id, niveau_id, annee_academique):
    """Récupère les matières pour une filière, niveau et année donnés"""
    try:
        matieres = list(Matiere.objects.filter(
            classe__filiere_id=filiere_id,
            classe__niveau_id=niveau_id,
            classe__annee_academique=annee_academique
        ).distinct().values('id', 'nom'))

        print(f"Debug - Filière: {filiere_id}, Niveau: {niveau_id}, Année: {annee_academique}")
        print(f"Debug - Matières trouvées: {matieres}")

        return JsonResponse(matieres, safe=False)
    except Exception as e:
        print(f"Erreur dans obtenir_matieres: {e}")
        return JsonResponse({'error': 'Erreur lors de la récupération des matières'}, status=500)

def document_list(request):
    """Vue pour lister les documents"""
    documents = PublicDocument.objects.all().order_by('-created_at')
    return render(request, 'base/documents.html', {'documents': documents})
