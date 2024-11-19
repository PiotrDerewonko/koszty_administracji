from django.contrib.auth.decorators import login_required
from ..forms import form_for_automatic_energy_meters
from django.shortcuts import render, redirect
from ..add_readings.add_meter_reading import add_meter_reading_automatic
from ..add_readings.modificate_data import data_from_xlx
from django.urls import reverse_lazy
from ..add_readings.energy_consumption import delete_energy_consumption, add_energy_consumption


@login_required
def add_metere_readings_from_xlsx(request):
    """widok, ktorego zadaniem jest przyjeceie pliku xlsx, odczytanie jego zawartosci a nastepnie zapis
    przekazanych danych do bazy danych."""
    form = form_for_automatic_energy_meters()
    if request.method == 'POST':
        month = request.POST.get('month')
        year = request.POST.get('year')
        file = request.FILES.get('file_with_meter_readings')
        pk = add_meter_reading_automatic(month, year, file)
        data_from_xlx(file, pk, request.user)
        delete_energy_consumption(int(year), int(month))
        add_energy_consumption(int(year), int(month))
        return redirect(reverse_lazy('electricity_cost:lista_odczytów'))

    return render(request, 'electricity_cost/add_meter_readings_automatic.html', context={'form': form})
