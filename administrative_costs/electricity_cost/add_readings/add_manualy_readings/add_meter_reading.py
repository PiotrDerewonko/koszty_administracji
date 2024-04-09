from django.shortcuts import render
from django.db import IntegrityError
from django.db.utils import Error

from ...models import MeterReadingsList


def add_meter_reading(month, year, date_of_read, photo, error_message) -> str:
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
        except:
            instance_month_year.add_manualy = True
            instance_month_year.save()

    except MeterReadingsList.DoesNotExist:
        meter_reading_list_instance = MeterReadingsList.objects.create(**dict_to_save)

    return error_message
