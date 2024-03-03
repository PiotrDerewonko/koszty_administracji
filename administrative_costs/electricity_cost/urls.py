from django.urls import path
from django.http import HttpResponse

app_name = 'electricity_cost'

urlpatterns = [
    path("", HttpResponse('helo')),
]
