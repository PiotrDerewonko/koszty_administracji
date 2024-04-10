from typing import List

import pandas as pd

from ..models import MeterReadingsList, MeterReading, EnergyMeters
from django.core.exceptions import ObjectDoesNotExist


def find_previous_period(year, month) -> [int, int]:
    """funkcja znajduje wczesniejszy okres rozliczeniowy. Zalozenie jest takie ze zachowana jest ciaglosc
    okresow rozliczeniowych."""
    if month > 1:
        year_to_return = year
        month_to_return = month - 1
    else:
        year_to_return = year - 1
        month_to_return = 12

    return year_to_return, month_to_return


def find_period_data(year: int, month: int):
    """Zadaniem funkcji jest zwrot danych z zadanego okresu w postaci df."""
    try:
        pk_reading_list = MeterReadingsList.objects.get(biling_year=year, biling_month=month)
        data = MeterReading.objects.filter(reading_name=pk_reading_list.id).values()
    except ObjectDoesNotExist:
        data = None

    return data


def compare_data(data_current, data_previous) -> str:
    """funkcja ktorej zadaniem jest porownanie danych z biezacego okresu, z danymi za okres poprzedni.
    Na pocztaku tworeze slownik dla df ze wszystkimi wartosciami z POST, nastepnie pobieram wartosci ze slwonika
    licnzikow i zostawiam sama wartosci licznikow a na koncu porownuje dane z biezace i dane poprzednie """

    tmp_dict = {'name': [], 'values': []}
    for i, j in data_current.POST.items():
        tmp_dict['name'].append(i)
        tmp_dict['values'].append(j)

    # pobieram slownik licznikow i tworze z niego df
    data_from_energy_meters = EnergyMeters.objects.all().values()
    energy_meters = pd.DataFrame.from_dict(data_from_energy_meters)
    energy_meters = energy_meters['name'].to_frame()
    energy_meters['is_good'] = True

    # tworze df z biezacych danych i odfitrowuje tylko dane z licnzikami
    data_current_from_dict = pd.DataFrame(data=tmp_dict)
    check_current_data = pd.merge(data_current_from_dict, energy_meters, how='left', on='name')
    good_data_current = check_current_data[check_current_data['is_good'] == True]

    #tworze df z poprzednimy danymi
    data_previous_df = pd.DataFrame.from_dict(data_previous)

    check_previous_data = pd.merge(data_previous_df, energy_meters, how='left', left_on='energy_meter_id',
                                   right_index=True)
    filtered_data_previous = check_previous_data[['name', 'meter_reading']]

    #tworzed df z porownaniem danych biezacych i poprzednich
    data_diffrent = pd.merge(good_data_current, filtered_data_previous, how='left', on='name')
    data_diffrent.drop(columns=['is_good'], inplace=True)
    data_diffrent.rename(columns={'values': 'dane teraz wpisane', 'meter_reading': 'dane w bazie danych'}, inplace=True)
    data_diffrent['dane teraz wpisane'].fillna(0, inplace=True)
    data_diffrent['dane w bazie danych'].fillna(0, inplace=True)
    data_diffrent['dane w bazie danych'] = data_diffrent['dane w bazie danych'].astype(float)
    data_diffrent['dane teraz wpisane'] = data_diffrent['dane teraz wpisane'].astype(float)
    data_diffrent['różnica'] = data_diffrent['dane teraz wpisane'] - data_diffrent['dane w bazie danych']
    return data_diffrent.to_html()

