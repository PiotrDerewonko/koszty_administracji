from validators import ValidationError

from ..models import EnergyMeters
from django.contrib.auth.decorators import login_required
from ..forms import get_energy_meter_form
from django.shortcuts import render, redirect
from ..add_readings.energy_consumption import delete_energy_consumption, add_energy_consumption
from ..add_readings.add_meter_reading import add_meter_reading_manualy, change_add_manualy, find_month_year
from ..add_readings.find_previous_period import find_period_data, find_next_period
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
        original_form_date = request.session['original_form_date']
        try:
            original_form_image = request.session['original_form_image']
            request.session.pop('original_form_image', None)
        except KeyError:
            original_form_image = None
        request.session.pop('original_form_data', None)
        request.session.pop('original_form_pk', None)
        request.session.pop('original_form_date', None)

    except KeyError:
        original_form_data = None
        original_form_pk = None
        original_form_date = None

    if request.method == 'POST' and pk is None and original_form_pk is None:
        form = energymeterform(request.POST)
        # to jest przypadek dla post gdzie jest on przesylany pierwszy raz
        if error_message == 'true':
            save_data_meter_readings(energymeterform, pk)
        else:
            if form.is_valid():
                month = request.POST.get('month')
                year = request.POST.get('year')
                date_of_read = request.POST.get('date_of_read')
                photo = request.FILES.get('image')
                if pk is not None:
                    delete_data(pk, is_add_manualy)
                else:
                    error_message, pk_mrl = add_meter_reading_manualy(month, year, date_of_read, photo, error_message)
                    if pk_mrl == 0:
                        return render(request, 'electricity_cost/add_meter_readings_manualy.html',
                                      {'form': form, 'error_message': error_message,

                                       'komunikat': '''Brak ciągłości danych. Brak danych za poprzedni okres rozliczeniowy.'''})
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
                        # change_add_manualy(month, year)
                        return render(request, 'electricity_cost/add_meter_readings_manualy.html',
                                      {'form': form, 'error_message': error_message,
                                       'data_diffrent': data_diffrent.to_html(index=False),
                                       'komunikat': 'Dane sa podejrzane'})
                    else:
                        save_data_meter_readings(request, pk_mrl)
                        add_energy_consumption(int(year), int(month))
                        return redirect(reverse_lazy('electricity_cost:lista_odczytów'))
    elif request.method != 'POST' and pk is not None:
        # to jest przypadek dla guzika edytuj dane, pokazuje dane jakie sa zapisane dla danego okresu
        data_static, data_dynamic = download_data_to_edit_manual_meter_readings(pk, manualy)
        energymeterform = get_energy_meter_form(energy_meter_fields, data_static=data_static, data_dynamic=data_dynamic,
                                                is_disable=True)
        form = energymeterform()
    elif request.method == 'POST' and original_form_pk is not None:
        # to jest przypadek gdzie przeslany jest post oraz zostal zaakceptowanyny dodatkowy formularz
        delete_data(original_form_pk, manualy)
        year, month = find_month_year(original_form_pk)
        save_data_meter_readings(original_form_data, original_form_pk)
        add_energy_consumption(year, month)
        change_data_in_meter_reading_list(original_form_pk, original_form_date, original_form_image)
        return redirect(reverse_lazy('electricity_cost:lista_odczytów'))
    elif request.method == 'POST' and pk is not None:
        # todo do wymyslenia jak polaczyc to z pierwsza opjca w tym widoku
        # to jest przypadek przeslanyh wydetywanych danych
        delete_data(pk, manualy)
        save_data_meter_readings(request, pk)
        year, month = find_month_year(pk)
        add_energy_consumption(year, month)
        try:
            next_year, next_month = find_next_period(year, month)
            add_energy_consumption(next_year, next_month)
        except IndexError:
            pass  # nie trzeba nic robic
        change_data_in_meter_reading_list(pk, request.POST.get('date_of_read'), request.FILES.get('image'))
        return redirect(reverse_lazy('electricity_cost:lista_odczytów'))
    else:
        form = energymeterform()

    return render(request, 'electricity_cost/add_meter_readings_manualy.html', {'form': form})
