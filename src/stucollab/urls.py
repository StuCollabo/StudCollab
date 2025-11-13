
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
  path('admin/', admin.site.urls),
  path('me/', include('users.urls')),
  path('my-groups/', include('groups.urls')),
  path('collab/', include('collab.urls')),
  path('', include('base.urls')), 


]
