from django.views.generic import ListView
from .models import Invoices, EnergyMeters
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import get_energy_meter_form
from django.shortcuts import render, redirect
from .add_manualy_readings.add_meter_reading import add_meter_reading


@method_decorator(login_required, name='dispatch')
class InvoicesListView(ListView):
    # todo dorobic filtrowanie faktur
    """Widok listy faktur oparty na ListView. Widok ma slużyć do przeglądania oraz sortowania faktur. Dodatkowo
    formularz ma dawac mozliwosc przejscie do edycji danej faktury, a w przyszlosci filtrownia faktur"""
    model = Invoices
    template_name = 'electricity_cost/invoices_view.html'
    paginate_by = 20
    ordering = ['-id']  # Ustawienie domyślnego sortowania

    def get_queryset(self):
        """
         Pobiera zapytanie dla listy faktur.
         Sortuje faktury zgodnie z parametrem sort, jeśli jest dostępny.
        """
        queryset = super().get_queryset()
        # Pobranie wartości parametru sort z adresu URL
        sort_param = self.request.GET.get('sort')
        if sort_param:
            # Wykonanie sortowania na podstawie parametru sort
            queryset = queryset.order_by(sort_param)
        return queryset

    def get_context_data(self, **kwargs):
        '''
        pobiera parametr sort
        '''
        context = super().get_context_data(**kwargs)
        sort_param = self.request.GET.get('sort', 'cost')
        context['sort'] = sort_param
        return context


@login_required
def add_meter_readings_maunaly(request):
    """
    widok dodawania recznego listy faktur. Do formualrza trafia aktualna lista licznikow z modelu, poczym jest
    generoweany formularz ktory zawiera wszystkie aktualne liczniki.
    """
    energy_meter_fields = EnergyMeters.objects.all()
    energymeterform = get_energy_meter_form(energy_meter_fields)
    error_message = None
    if request.method == 'POST':
        form = energymeterform(request.POST)
        if form.is_valid():
            month = request.POST.get('month')
            year = request.POST.get('year')
            date_of_read = request.POST.get('date_of_read')
            photo = request.FILES.get('photo')
            error_message = add_meter_reading(month, year, date_of_read, photo, error_message)
            return render(request, 'electricity_cost/add_meter_readings_manualy.html',
                          {'form': form, 'error_message': error_message})




    else:
        form = energymeterform()

    return render(request, 'electricity_cost/add_meter_readings_manualy.html', {'form': form})
