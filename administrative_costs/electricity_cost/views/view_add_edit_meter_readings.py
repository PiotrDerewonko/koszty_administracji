from django.views.generic import ListView
from ..models import Invoices, EnergyMeters, MeterReading, Year, Month, MeterReadingsList
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from ..forms import get_energy_meter_form
from django.shortcuts import render, redirect
from ..add_readings.add_manualy_readings.add_meter_reading import add_meter_reading
from ..add_readings.find_previous_period import find_previous_period, find_period_data
from ..add_readings.modificate_data import (find_wrond_energy_meters_reading, compare_data, save_data_meter_readings,
                                            delete_data, change_data_in_meter_reading_list)
from ..add_readings.download_data import download_data_to_edit_manual_meter_readings
from django.urls import reverse_lazy
from django.utils.datastructures import MultiValueDictKeyError
import json

@login_required
def add_edit_meter_readings(request, pk=None):
    """
    widok dodawania recznego listy faktur. Do formualrza trafia aktualna lista licznikow z modelu, poczym jest
    generoweany formularz ktory zawiera wszystkie aktualne liczniki.
    """
    energy_meter_fields = EnergyMeters.objects.filter(is_add_manual=True)
    energymeterform = get_energy_meter_form(energy_meter_fields)
    try:
        error_message = request.POST['error_message']
        a= 56
    except MultiValueDictKeyError as e:
        error_message = None
    if request.method == 'POST' and pk is None:
        form = energymeterform(request.POST)
        if error_message == 'true':
            print(request.session['original_form'])
            save_data_meter_readings(energymeterform, pk)
        else:
            if form.is_valid():
                month = request.POST.get('month')
                year = request.POST.get('year')
                date_of_read = request.POST.get('date_of_read')
                photo = request.FILES.get('photo')
                error_message, pk_mrl = add_meter_reading(month, year, date_of_read, photo, error_message)
                if error_message == 'manual_exist':
                    previous_data = find_period_data(int(year), int(month))
                    compared_data = compare_data(request, previous_data, 'dane teraz wpisane',
                                                 'dane w bazie danych')
                    #todo do wymyslenia jak zapisac te dane w sesji moze petla i po nazwach?
                    request.session['original_form'] = json.dumps(form.cleaned_data)
                    return render(request, 'electricity_cost/add_meter_readings_manualy.html',
                                  {'form': form, 'error_message': error_message,
                                   'data_diffrent': compared_data.to_html(index=False),
                                   'komunikat': '''Dane za ten okres rozliczeniowy były już dodawane, Jeśli mimo to chcesz nadpisać dane wybierz zapisz.
                Jeśli chcesz cofnąć się to wypełnionego formularza wybierz anuluj.'''})
                else:
                    data_diffrent, error_message = find_wrond_energy_meters_reading(request, year, month)
                    if error_message == 'wrong_insert_data':
                        return render(request, 'electricity_cost/add_meter_readings_manualy.html',
                                      {'form': form, 'error_message': error_message,
                                       'data_diffrent': data_diffrent.to_html(index=False),
                                       'komunikat': 'Dane sa podejrzane'})
                    else:
                        save_data_meter_readings(request, pk_mrl)
                        return redirect(reverse_lazy('electricity_cost:lista_odczytów'))
    elif request.method != 'POST' and pk is not None:
        data_static, data_dynamic = download_data_to_edit_manual_meter_readings(pk)
        energymeterform = get_energy_meter_form(energy_meter_fields, data_static=data_static, data_dynamic=data_dynamic)
        form = energymeterform()
    elif request.method == 'POST' and pk is not None:
        delete_data(pk, True)
        save_data_meter_readings(request, pk)
        change_data_in_meter_reading_list(pk, request)
        return redirect(reverse_lazy('electricity_cost:lista_odczytów'))
    else:
        form = energymeterform()

    return render(request, 'electricity_cost/add_meter_readings_manualy.html', {'form': form})
