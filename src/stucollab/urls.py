from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView

urlpatterns = [
  path('admin/', admin.site.urls),
  path('me/', include('users.urls')),
  path('my-groups/', include('groups.urls')),
  path('collab/', include('collab.urls')),
  path('', include('base.urls')), 
  path('logout/', LogoutView.as_view(next_page="home"), name="logout"),


]
