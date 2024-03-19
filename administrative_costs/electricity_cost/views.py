from django.views.generic import ListView
from .models import Invoices, EnergyMeters
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import get_energy_meter_form
from django.shortcuts import render, redirect


@method_decorator(login_required, name='dispatch')
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

@login_required
def add_metere_readings_maunaly(request):
    energy_meter_fields = EnergyMeters.objects.all()
    EnergyMeterForm = get_energy_meter_form(energy_meter_fields)
    if request.method == 'POST':
        form = EnergyMeterForm(request.POST)
        if form.is_valid():
            # Obsłuż dane z formularza
            pass
    else:
        form = EnergyMeterForm()

    return render(request, 'electricity_cost/add_meter_readings_manualy.html', {'form': form})