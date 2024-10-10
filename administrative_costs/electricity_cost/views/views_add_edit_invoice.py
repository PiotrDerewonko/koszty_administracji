from django.views.generic import CreateView, UpdateView
from django.contrib.auth.decorators import login_required
from ..models import Invoices
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy


@method_decorator(login_required, name='dispatch')
class InvoicesAddInvoiceView(CreateView):
    model = Invoices
    template_name = 'electricity_cost/add_invoice.html'
    fields = ['invoices_number', 'cost', 'numbers_mwh', 'energysuppliers', 'biling_month', 'biling_year',
              'type_of_invoice']
    success_url = reverse_lazy('electricity_cost:lista_faktur')

    def form_valid(self, form):
        # Pobieramy wartości z formularza
        total_cost = form.cleaned_data.get('cost')
        mwh = form.cleaned_data.get('numbers_mwh')

        # Obliczamy koszt za 1 kWh
        if mwh and mwh > 0:
            cost_per_mwh = total_cost / mwh
            form.instance.cost_per_1_mwh = cost_per_mwh

        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class EditInvoiceView(UpdateView):
    model = Invoices
    template_name = 'electricity_cost/add_invoice.html'
    fields = ['invoices_number', 'cost', 'numbers_mwh', 'energysuppliers', 'biling_month', 'biling_year',
              'type_of_invoice']
    success_url = reverse_lazy('electricity_cost:lista_faktur')

    def form_valid(self, form):
        # Pobieramy wartości z formularza
        total_cost = form.cleaned_data.get('cost')
        mwh = form.cleaned_data.get('numbers_mwh')

        # Obliczamy koszt za 1 kWh
        if mwh and mwh > 0:
            cost_per_mwh = total_cost / mwh
            form.instance.cost_per_1_mwh = cost_per_mwh

        return super().form_valid(form)
