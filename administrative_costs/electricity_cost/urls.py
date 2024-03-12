from django.urls import path
from .models import Invoices
from .views import InvoicesListView

app_name = 'electricity_cost'

urlpatterns = [
    path("faktury/",
         InvoicesListView.as_view(), name='lista_faktur'),
]
