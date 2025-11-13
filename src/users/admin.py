from django.contrib import admin
from fichiers.models import Faculte, Filiere, Matiere, Niveau, Classe
from utilisateurs.models import  CustomUser
from groups.models import Group
admin.site.register(Faculte)
admin.site.register(Filiere)
admin.site.register(Matiere)
admin.site.register(Niveau)
admin.site.register(Classe)
admin.site.register(CustomUser)
admin.site.register(Group)
