from django.contrib import admin
from users.models import User
from groups.models import Group


admin.site.register(User)
admin.site.register(Group)
