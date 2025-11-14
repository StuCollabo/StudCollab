from django.shortcuts import render
from users.models import User

def get_home(request):
  count_users = User.objects.all().count()
  context = {"count_users":count_users}

  return render(request, "base/home.html", context)
