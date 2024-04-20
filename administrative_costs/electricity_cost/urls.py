from django.urls import path
from .models import Invoices
from .views.view_add_edit_meter_readings import add_edit_meter_readings
from .views.views_list import InvoicesListView, EnergyReadingsView

app_name = 'electricity_cost'

urlpatterns = [
    path("faktury/", InvoicesListView.as_view(), name='lista_faktur'),
    path('add/', add_edit_meter_readings, name='dodawanie_reczne_licznikow'),
    path('add/<int:pk>/', add_edit_meter_readings, name='edycja_reczna_licznikow'),
    path('odczyty/', EnergyReadingsView.as_view(), name='lista_odczytów')
]
