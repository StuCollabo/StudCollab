from django.db import models
from users.models import User
from groups.models import Group
import hashlib
from django.core.exceptions import ValidationError


class ActivityLog(models.Model):
  group = models.ForeignKey(Group, on_delete=models.CASCADE)
  user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
  action = models.CharField(max_length=255)
  created_at = models.DateTimeField(auto_now_add=True)

class Task(models.Model):
  group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='tasks')
  title = models.CharField(max_length=255)
  assigned_to = models.ForeignKey(User, null=True,
    blank=True, on_delete=models.SET_NULL)
  completed = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f"{self.title} - {self.assigned_to.username}"


class BaseDocument(models.Model):
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to='documents/')
    hash = models.CharField(max_length=64, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    url = models.URLField(max_length=500, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,
      null=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.hash and self.file:
            self.file.seek(0)
            file_data = self.file.read()
            self.hash = hashlib.sha256(file_data).hexdigest()
            self.file.seek(0)

        if self.file and not self.url:
            self.url = self.file.url

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title}"


class GroupDocument(BaseDocument):
  group = models.ForeignKey(Group,
    on_delete=models.CASCADE)
  is_pub = models.BooleanField(default=False)

"""
  def clean(self):
    if not self.group:
      raise ValidationError("This document should be assigned to a group.")
"""


class Notification(models.Model):
  task = models.ForeignKey(Task, on_delete=models.CASCADE)
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications_received")
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  triggered_by = models.ManyToManyField(User, related_name="notifications_triggered")

  def __str__(self):
    return self.task.title
