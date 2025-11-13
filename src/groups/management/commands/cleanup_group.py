from django.core.management.base import BaseCommand
from utilisateurs.models import Group

class Command(BaseCommand):
  help = "Supprime les groupes..."
  def handle(self, *args, **options):
    pass
