from django.urls import path
from .models import Invoices
from .views.view_add_edit_meter_readings import add_edit_meter_readings
from .views.view_add_xlsx import add_metere_readings_from_xlsx
from .views.views_list import InvoicesListView, EnergyReadingsView
from .views.views_add_edit_invoice import InvoicesAddInvoiceView, EditInvoiceView, DeleteInvoiceView

app_name = 'electricity_cost'

urlpatterns = [
    path("faktury/", InvoicesListView.as_view(), name='lista_faktur'),
    path('add/<str:is_add_manualy>/', add_edit_meter_readings, name='dodawanie_reczne_licznikow'),
    path('add/<int:pk>/<str:is_add_manualy>/', add_edit_meter_readings, name='edycja_odczytow_licznikow'),
    path('odczyty/', EnergyReadingsView.as_view(), name='lista_odczytów'),
    path('add_automat/', add_metere_readings_from_xlsx, name='dodawanie_automatyczne_odczytow'),
    path('add_invoice/', InvoicesAddInvoiceView.as_view(), name='dodawanie_faktury'),
    path('edit_invoice/<int:pk>', EditInvoiceView.as_view(), name='edycja_faktury'),
    path('delete_invoice/<int:pk>/delete/', DeleteInvoiceView.as_view(), name='usuwanie_faktury')
]
