# views.py
from django.contrib.auth import logout as django_logout
from django.shortcuts import redirect

def custom_logout(request):
    django_logout(request)
    return redirect('login')
