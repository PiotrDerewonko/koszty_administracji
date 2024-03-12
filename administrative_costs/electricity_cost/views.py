from django.views.generic import ListView
from .models import Invoices
from django.core.paginator import Paginator


class InvoicesListView(ListView):
    model = Invoices
    template_name = 'electricity_cost/invoices_view.html'
    paginate_by = 20
    ordering = ['-id']  # Ustawienie domyślnego sortowania

    def get_queryset(self):
        queryset = super().get_queryset()
        # Pobranie wartości parametru sort z adresu URL
        sort_param = self.request.GET.get('sort')
        if sort_param:
            # Wykonanie sortowania na podstawie parametru sort
            queryset = queryset.order_by(sort_param)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sort_param = self.request.GET.get('sort', 'cost')  # Domyślna wartość sortowania
        context['sort'] = sort_param
        return context
