from django.db import models
from users.models import User
import uuid

class Group(models.Model):
  name = models.CharField(max_length=200)
  members = models.ManyToManyField(User, related_name="GroupUser")
  invit_code = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
  creator = models.ForeignKey(User, on_delete=models.CASCADE,
    related_name="groupes_crees", null=True)
  created_at = models.DateTimeField(auto_now_add=True)
  expires_at = models.DateTimeField(null=True, blank=True)
  storage_used = models.BigIntegerField(default=0)
  is_active = models.BooleanField(default=True)

  def __str__(self):
    return self.name


class SubGroup(models.Model):
  name = models.CharField(max_length=200)
  members = models.ManyToManyField(User, related_name="SubGroupUser")
  invit_code = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
  creator = models.ForeignKey(User, on_delete=models.SET_NULL,
    related_name="subgroups_created", null=True)
  head = models.ForeignKey(User, on_delete=models.SET_NULL,
    related_name="groupes_chef", null=True)
  group = models.ForeignKey(Group, on_delete=models.CASCADE)

  def __str__(self):
    return self.name
