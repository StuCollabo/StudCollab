from django import forms
from django.conf import settings
from fichiers.models import PublicDocument, DocumentType, Matiere, Faculte, Filiere, Niveau

def get_annee_choices():
    """Génère la liste des années académiques disponibles"""
    ANNEE_FIN = getattr(settings, 'ANNEE_FIN', 35)
    return [(f"20{i}-20{i+1}", f"20{i}-20{i+1}") for i in range(20, ANNEE_FIN)]

class TeleverserForm(forms.ModelForm):
    # Champs additionnels pour le filtrage
    faculte = forms.ModelChoiceField(
        queryset=Faculte.objects.all(),
        required=True,
        empty_label="Sélectionnez une faculté",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    # NOUVEAU : Champ Niveau
    niveau = forms.ModelChoiceField(
        queryset=Niveau.objects.all(),
        required=True,
        empty_label="Sélectionnez un niveau",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    annee_academique = forms.ChoiceField(
        choices=[('', 'Sélectionnez une année')] + get_annee_choices(),
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    filiere = forms.ModelChoiceField(
        queryset=Filiere.objects.none(),
        required=True,
        empty_label="Sélectionnez une filière",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    matiere = forms.ModelChoiceField(
        queryset=Matiere.objects.none(),
        required=True,
        empty_label="Sélectionnez la matière",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    type = forms.ModelChoiceField(
        queryset=DocumentType.objects.all(),
        required=False,
        empty_label="Quel genre de document est-ce?",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = PublicDocument
        fields = ["title", "subject", "type", "file"]
        exclude = ["hash", "created_at", "url"]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Title of document'
            }),
            'file': forms.ClearableFileInput(attrs={
                'id': 'fileInput',
                'style': 'display:none;'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Initialisation des querysets vides
        self.fields["filiere"].queryset = Filiere.objects.none()
        self.fields["matiere"].queryset = Matiere.objects.none()

        # Si on a des données POST, on filtre selon les sélections
        if 'faculte' in self.data and 'niveau' in self.data and 'annee_academique' in self.data:
            try:
                faculte_id = int(self.data.get('faculte'))
                niveau_id = int(self.data.get('niveau'))
                annee_academique = self.data.get('annee_academique')

                # Filtrage des filières par faculté, niveau ET année
                self.fields['filiere'].queryset = Filiere.objects.filter(
                    faculte_id=faculte_id,
                    classe__niveau_id=niveau_id,
                    classe__annee_academique=annee_academique
                ).distinct()

            except (ValueError, TypeError):
                pass

        if 'filiere' in self.data and 'niveau' in self.data and 'annee_academique' in self.data:
            try:
                filiere_id = int(self.data.get('filiere'))
                niveau_id = int(self.data.get('niveau'))
                annee_academique = self.data.get('annee_academique')

                # Filtrage des matières par filière, niveau ET année
                self.fields["matiere"].queryset = Matiere.objects.filter(
                    classe__filiere_id=filiere_id,
                    classe__niveau_id=niveau_id,
                    classe__annee_academique=annee_academique
                ).distinct()

            except (ValueError, TypeError):
                pass

        # Si on modifie un document existant
        elif self.instance.pk and hasattr(self.instance, 'matiere'):
            self.fields["matiere"].queryset = Matiere.objects.filter(
                pk=self.instance.matiere.pk
            )

    def clean(self):
        cleaned_data = super().clean()
        matiere = cleaned_data.get('matiere')
        filiere = cleaned_data.get('filiere')
        faculte = cleaned_data.get('faculte')
        niveau = cleaned_data.get('niveau')
        annee_academique = cleaned_data.get('annee_academique')

        # Vérification : la filière doit appartenir à la faculté
        if filiere and faculte:
            if filiere.faculte != faculte:
                raise forms.ValidationError(
                    "La filière sélectionnée n'appartient pas à la faculté choisie."
                )

        # Vérification : la combinaison filière/niveau/année doit exister dans une Classe
        if filiere and niveau and annee_academique:
            from fichiers.models import Classe
            classe_existe = Classe.objects.filter(
                filiere=filiere,
                niveau=niveau,
                annee_academique=annee_academique
            ).exists()
            
            if not classe_existe:
                raise forms.ValidationError(
                    f"Aucune classe trouvée pour {filiere.nom} - {niveau.niveau} - {annee_academique}"
                )

        return cleaned_data
