from django.shortcuts import render
from django.db import IntegrityError
from django.db.utils import Error
from django.core.exceptions import ValidationError

from ..models import MeterReadingsList


def add_meter_reading_manualy(month, year, date_of_read, photo, error_message) -> [str, int]:
    """Funkcja ktorej zadnaiem jest utworzenie nowej instancji modelu MeterReadingsList, a w wypadku gdy
    taka instancja juz istnieje sprawdzenie czy byly dodwane wartosci recznie a jesli tak to zwrocenie komunikatu bledu
    aby dac uzytkownikowi wybor czy chce dane nadpisac czy nie"""
    dict_to_save = {'photo': photo, 'date_of_read': date_of_read, 'biling_month_id': month,
                    'biling_year_id': year, 'add_manualy': True}
    try:
        instance_month_year = MeterReadingsList.objects.get(biling_month=month, biling_year=year)
        try:
            instance_month_year_add_manualy = MeterReadingsList.objects.get(biling_month=month, biling_year=year,
                                                                            add_manualy=True)
            error_message = 'manual_exist'


        except MeterReadingsList.DoesNotExist:
            instance_month_year.add_manualy = True
            instance_month_year.save()
        final_instance = MeterReadingsList.objects.get(biling_month=month, biling_year=year)
        final_instance_pk = final_instance.pk
    except MeterReadingsList.DoesNotExist:
        try:
            meter_reading_list_instance = MeterReadingsList.objects.create(**dict_to_save)
            final_instance = MeterReadingsList.objects.get(biling_month=month, biling_year=year)
            final_instance_pk = final_instance.pk
        except ValidationError as e:
            # Obsługa błędu ValidationError
            error_message = "wrong_previous_data"
            final_instance_pk = 0

    return error_message, final_instance_pk


def add_meter_reading_automatic(month, year, file) -> [int]:
    """Funkcja ktorej zadnaiem jest utworzenie nowej instancji modelu MeterReadingsList, a w wypadku gdy
    taka instancja juz istnieje sprawdzenie czy byly dodwane wartosci automatyczne"""
    dict_to_save = {'xlsx_file': file, 'biling_month_id': month,
                    'biling_year_id': year, 'add_automatic': True}

    try:
        instance_month_year = MeterReadingsList.objects.get(biling_month=month, biling_year=year)
        try:
            instance_month_year_add_automatic = MeterReadingsList.objects.get(biling_month=month, biling_year=year,
                                                                              add_manualy=False)

        except MeterReadingsList.DoesNotExist:
            instance_month_year.add_automatic = True
            instance_month_year.xlsx_file = file
            instance_month_year.save()

    except MeterReadingsList.DoesNotExist:
        meter_reading_list_instance = MeterReadingsList.objects.create(**dict_to_save)

    final_instance = MeterReadingsList.objects.get(biling_month=month, biling_year=year)
    final_instance_pk = final_instance.pk

    return final_instance_pk


def change_add_manualy(month, year) -> None:
    """Zadaniem funkcji jest zmiana parametru add_manualy na false gdy nie udalo sie zapisac danych."""
    instance_month_year = MeterReadingsList.objects.get(biling_month=month, biling_year=year)
    instance_month_year.add_manualy = False
    instance_month_year.save()


def find_month_year(pk) -> [int, int]:
    """Zadaniem funkcji jest odnalezienie jakiego miesiaca i roku obliczeniowwego dotyczy dane id listy odczytow."""
    instance_month_year = MeterReadingsList.objects.get(pk=pk)
    year_to_return = instance_month_year.biling_year_id
    month_to_return = instance_month_year.biling_month_id
    return year_to_return, month_to_return
