from django.urls import path
from .models import Invoices
from .views import InvoicesListView, add_meter_readings_maunaly

app_name = 'electricity_cost'

urlpatterns = [
    path("faktury/",InvoicesListView.as_view(), name='lista_faktur'),
    path('add/', add_meter_readings_maunaly, name='dodawanie_reczene_licznikow')
]
