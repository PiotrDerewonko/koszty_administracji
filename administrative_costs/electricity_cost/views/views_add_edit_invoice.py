from django.views.generic import CreateView, UpdateView
from django.contrib.auth.decorators import login_required
from ..models import Invoices
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy


@method_decorator(login_required, name='dispatch')
class InvoicesAddInvoiceView(CreateView):
    model = Invoices
    template_name = 'electricity_cost/add_invoice.html'
    fields = '__all__'
    success_url = reverse_lazy('electricity_cost:lista_faktur')

    def form_invalid(self, form):
        print(form.errors)  # Dodaj debugowanie, aby zobaczyć błędy formularza
        return super().form_invalid(form)


@method_decorator(login_required, name='dispatch')
class EditInvoiceView(UpdateView):
    model = Invoices
    template_name = 'electricity_cost/add_invoice.html'
    fields = '__all__'
    success_url = reverse_lazy('electricity_cost:lista_faktur')
