from django.contrib import admin
from users.models import User
from groups.models import Group
from collab.models import Notification

admin.site.register(User)
admin.site.register(Group)
admin.site.register(Notification)
