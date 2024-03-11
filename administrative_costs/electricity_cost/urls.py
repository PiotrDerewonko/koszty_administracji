from django.urls import path
from .models import Invoices
from django.views.generic import ListView

app_name = 'electricity_cost'

urlpatterns = [
    path("faktury/", ListView.as_view(model=Invoices, template_name='electricity_cost/invoices_view.html'),
         name='lista_faktur'),
]
