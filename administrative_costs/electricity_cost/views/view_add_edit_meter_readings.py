from ..models import EnergyMeters
from django.contrib.auth.decorators import login_required
from ..forms import get_energy_meter_form
from django.shortcuts import render, redirect
from ..add_readings.add_manualy_readings.add_meter_reading import add_meter_reading
from ..add_readings.find_previous_period import find_period_data
from ..add_readings.modificate_data import (find_wrond_energy_meters_reading, compare_data, save_data_meter_readings,
                                            delete_data, change_data_in_meter_reading_list, save_data_to_sesion)
from ..add_readings.download_data import download_data_to_edit_manual_meter_readings
from django.urls import reverse_lazy
from django.utils.datastructures import MultiValueDictKeyError


@login_required
def add_edit_meter_readings(request, pk=None, is_add_manualy=None):
    """
    widok dodawania oraz edycji licznikow dodawanych recznei, oraz edycji danych wprowadzanych automatycznie.
    Do formualrza trafia aktualna lista licznikow z modelu ale w zależności od przekazanaego parametru pokazywane
    sa odpowiednie liczniki.
    """
    if is_add_manualy.lower() == 'true':
        manualy = True
    elif is_add_manualy.lower() == 'false':
        manualy = False
    else:
        manualy = False
    energy_meter_fields = EnergyMeters.objects.filter(is_add_manual=manualy)
    energymeterform = get_energy_meter_form(energy_meter_fields)
    try:
        error_message = request.POST['error_message']
    except MultiValueDictKeyError as e:
        error_message = None
    try:
        original_form_data = request.session['original_form_data']
        original_form_pk = request.session['original_form_pk']
        original_form_image = request.session['original_form_image']
        original_form_date = request.session['original_form_date']
        request.session.pop('original_form_data', None)
        request.session.pop('original_form_pk', None)
        request.session.pop('original_form_image', None)
        request.session.pop('original_form_date', None)
    except KeyError:
        original_form_data = None
        original_form_pk = None
        original_form_image = None
        original_form_date = None
    if request.method == 'POST' and pk is None and original_form_pk is None:
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
                    compared_data, current_data_df = compare_data(request, previous_data, 'dane teraz wpisane',
                                                                  'dane w bazie danych')
                    save_data_to_sesion(current_data_df, request, pk_mrl)
                    return render(request, 'electricity_cost/add_meter_readings_manualy.html',
                                  {'form': form, 'error_message': error_message,
                                   'data_diffrent': compared_data.to_html(index=False),
                                   'komunikat': '''Dane za ten okres rozliczeniowy były już dodawane, 
                                   Jeśli mimo to chcesz nadpisać dane wybierz zapisz.
                Jeśli chcesz cofnąć się to wypełnionego formularza wybierz anuluj.'''})
                else:
                    data_diffrent, error_message, current_data_df = find_wrond_energy_meters_reading(request, year,
                                                                                                     month)
                    if error_message == 'wrong_insert_data':
                        save_data_to_sesion(current_data_df, request, pk_mrl)
                        return render(request, 'electricity_cost/add_meter_readings_manualy.html',
                                      {'form': form, 'error_message': error_message,
                                       'data_diffrent': data_diffrent.to_html(index=False),
                                       'komunikat': 'Dane sa podejrzane'})
                    else:
                        save_data_meter_readings(request, pk_mrl)
                        return redirect(reverse_lazy('electricity_cost:lista_odczytów'))
    elif request.method != 'POST' and pk is not None:
        data_static, data_dynamic = download_data_to_edit_manual_meter_readings(pk, manualy)
        energymeterform = get_energy_meter_form(energy_meter_fields, data_static=data_static, data_dynamic=data_dynamic,
                                                is_disable=True)
        form = energymeterform()
    elif request.method == 'POST' and original_form_pk is not None:
        delete_data(original_form_pk, manualy)
        save_data_meter_readings(original_form_data, original_form_pk)
        change_data_in_meter_reading_list(original_form_pk, original_form_image, original_form_date)
        return redirect(reverse_lazy('electricity_cost:lista_odczytów'))
    else:
        form = energymeterform()

    return render(request, 'electricity_cost/add_meter_readings_manualy.html', {'form': form})
