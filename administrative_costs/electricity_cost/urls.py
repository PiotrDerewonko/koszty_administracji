from django.urls import path
from .models import Invoices
from .views import InvoicesListView, add_meter_readings_maunaly, EnergyReadingsView

app_name = 'electricity_cost'

urlpatterns = [
    path("faktury/", InvoicesListView.as_view(), name='lista_faktur'),
    path('add/', add_meter_readings_maunaly, name='dodawanie_reczne_licznikow'),
    path('odczyty/', EnergyReadingsView.as_view(), name='lista_odczytów')
]
