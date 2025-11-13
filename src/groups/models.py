from django.db import models
from utilisateurs.models import CustomUser
import uuid

class Group(models.Model):
  name = models.CharField(max_length=200)
  members = models.ManyToManyField(CustomUser, related_name="GroupUser")
  invit_code = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
  creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
    related_name="groupes_crees", null=True)
  created_at = models.DateTimeField(auto_now_add=True)
  expires_at = models.DateTimeField(null=True, blank=True)
  storage_used = models.BigIntegerField(default=0)
  is_active = models.BooleanField(default=True)

  def __str__(self):
    return self.name
