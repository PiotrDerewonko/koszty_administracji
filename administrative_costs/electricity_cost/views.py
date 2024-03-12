from django.views.generic import ListView
from .models import Invoices

class InvoicesListView(ListView):
    model = Invoices
    template_name = 'electricity_cost/invoices_view.html'
    context_object_name = 'object_list'
    ordering = ['id']  # Ustawienie domyślnego sortowania

    def get_queryset(self):
        queryset = super().get_queryset()
        # Pobranie wartości parametru sort z adresu URL
        sort_param = self.request.GET.get('sort')
        if sort_param:
            # Wykonanie sortowania na podstawie parametru sort
            queryset = queryset.order_by(sort_param)
        return queryset
