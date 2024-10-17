import pandas as pd
from ..models import EnergyMeters, MeterReading, MeterReadingsList
from .find_previous_period import find_previous_period, find_period_data
import json
from django.utils.datastructures import MultiValueDictKeyError
from typing import Dict


def change_form_to_df(data) -> pd.DataFrame:
    """funkcja zamienia przekazane dane z formularza (z request) lub slwonika na dataframe"""
    tmp_dict = {'name': [], 'values': []}
    if isinstance(data, dict):
        for key, value in data.items():
            tmp_dict['name'].append(key)
            tmp_dict['values'].append(value)
        data_current_from_dict = pd.DataFrame(data=tmp_dict)
    elif isinstance(data, pd.DataFrame):
        data_current_from_dict = data
    else:
        for i, j in data.POST.items():
            tmp_dict['name'].append(i)
            tmp_dict['values'].append(j)
        data_current_from_dict = pd.DataFrame(data=tmp_dict)

    return data_current_from_dict


def modificate_energy_meters_dict() -> pd.DataFrame:
    """Funkcja zwraca dataframe z nazwami licznikow """
    data_from_energy_meters = EnergyMeters.objects.all().values()
    energy_meters = pd.DataFrame.from_dict(data_from_energy_meters)
    energy_meters = energy_meters[['name', 'id']]
    energy_meters['is_good'] = True
    return energy_meters


def filtr_only_energy_meters_from_request(data) -> pd.DataFrame:
    """funckja zwraca dataframe z przekazanych wartosci z request post, ktore wystepuja w slowniku licznikow"""
    data_df = change_form_to_df(data)
    em_df = modificate_energy_meters_dict()
    data_all = pd.merge(data_df, em_df, how='left', on='name')
    data_all = data_all[data_all['is_good'] == True]
    data_all.drop('is_good', axis=1, inplace=True)
    return data_all


def find_wrond_energy_meters_reading(data_from_form, year: int, month: int) -> [pd.DataFrame, str, pd.DataFrame]:
    """Zadaniem tej funkcji jest porownanie przekazanych danych z poprzednim okresem rozliczeniowym i odfiltrowanie
    danych ktore moga byc bledne np, wartosc odczytu w biezacym miesiacu jest mniejsza niz w poprzednim, lub
    jest duzo wieksza."""
    error_massage = None
    previous_year, previous_month = find_previous_period(int(year), int(month))
    previous_data = find_period_data(previous_year, previous_month)
    if previous_data is not None:
        compared_data, good_data = compare_data(data_from_form, previous_data, 'Dane z bieżącego okresu',
                                                'Dane z poprzedniego okresu')
        filtered_compared_data = compared_data.loc[(compared_data['różnica'] < 0)]
        if len(filtered_compared_data) > 0:
            error_massage = 'wrong_insert_data'
    else:
        filtered_compared_data = None
        good_data = None
        error_massage = 'test'
    return filtered_compared_data, error_massage, good_data


def compare_data(data_current, data_previous, label_cuurent_data, label_prevoius_data) -> pd.DataFrame:
    """funkcja ktorej zadaniem jest porownanie danych z biezacego okresu, z danymi za okres poprzedni.
    Na pocztaku tworeze slownik dla df ze wszystkimi wartosciami z POST, nastepnie pobieram wartosci ze slwonika
    licnzikow i zostawiam sama wartosci licznikow a na koncu porownuje dane z biezace i dane poprzednie """

    # pobieram slownik licznikow i tworze z niego df
    energy_meters = modificate_energy_meters_dict()

    # tworze df z biezacych danych i odfitrowuje tylko dane z licnzikami
    data_current_from_dict = change_form_to_df(data_current)
    check_current_data = pd.merge(data_current_from_dict, energy_meters, how='left', on='name')
    good_data_current = check_current_data.loc[check_current_data['is_good'] == True]

    # tworze df z poprzednimy danymi
    data_previous_df = pd.DataFrame.from_dict(data_previous)

    if len(data_previous_df) > 0:
        check_previous_data = pd.merge(data_previous_df, energy_meters, how='left', left_on='energy_meter_id',
                                       right_on='id')
        filtered_data_previous = check_previous_data[['name', 'meter_reading']]

        # tworzed df z porownaniem danych biezacych i poprzednich
        data_diffrent = pd.merge(good_data_current, filtered_data_previous, how='left', on='name')
        data_diffrent.drop(columns=['is_good'], inplace=True)
        data_diffrent.rename(columns={'values': label_cuurent_data, 'meter_reading': label_prevoius_data,
                                      'name': 'nazwa licznika'}, inplace=True)
        data_diffrent[label_cuurent_data].fillna(0, inplace=True)
        data_diffrent[label_prevoius_data].fillna(0, inplace=True)
        data_diffrent[label_prevoius_data] = data_diffrent[label_prevoius_data].astype(float)
        data_diffrent[label_cuurent_data] = data_diffrent[label_cuurent_data].astype(float)
        data_diffrent['różnica'] = data_diffrent[label_cuurent_data] - data_diffrent[label_prevoius_data]
    else:
        data_diffrent = pd.DataFrame()
    return data_diffrent, good_data_current


def save_data_meter_readings(data, key) -> None:
    """Funkcja zapisuje dane przekazane w formualrzu do taberli z odczytami licznikow. Dane tu zawarte, to
    wylacznie odczyty licznikow bez dat i okresow rozliczeniowych."""
    data_to_save = filtr_only_energy_meters_from_request(data)
    data_to_save['reading_name_id'] = key
    data_to_save.rename(columns={'values': 'meter_reading', 'id': 'energy_meter_id'}, inplace=True)
    data_to_save.drop(columns=['name'], inplace=True)
    data_to_save_json = data_to_save.to_json(orient='records')
    data_to_save_json = json.loads(data_to_save_json)
    # Iteracja po słownikach i zapisanie każdego jako osobnego obiektu MeterReading
    for item in data_to_save_json:
        MeterReading.objects.create(
            meter_reading=item['meter_reading'],
            energy_meter_id=item['energy_meter_id'],
            reading_name_id=item['reading_name_id']
        )


def delete_data(pk, is_manual) -> None:
    """Funkcja ta kasuje dane z wybranego odczytu. parametr is_manual okresla czy skasowane maja zostac odczyty licznikow
    dodawaanych recznie czy tez odczyty dodawane automatycznie."""
    try:
        records_to_delete = MeterReading.objects.filter(reading_name_id=pk, energy_meter_id__in=
        EnergyMeters.objects.filter(is_add_manual=is_manual))
        records_to_delete.delete()
    except MeterReading.DoesNotExist:
        pass  # nie potrzeba podejmowac dalszych dzialan


def change_data_in_meter_reading_list(pk, data_of_read, image) -> None:
    """Funkcja zmienia wartosc modelu na przekazane dane"""
    data_to_change = MeterReadingsList.objects.get(id=pk)
    data_to_change.date_of_read = data_of_read
    if image:
        data_to_change.photo = image
    data_to_change.save()


def change_data_to_dict(data) -> Dict:
    dict_to_return = {}
    data.set_index('name', inplace=True)
    for i, j in data['values'].items():
        dict_to_return[i] = j
    return dict_to_return


def save_data_to_sesion(current_data_df, request, pk_mrl) -> None:
    """Funckja zapisuje w sesji dane potrzebne do ewentualnego zapisu po zatwierdzeniu przez uzytkownika"""
    dict_with_data_from_form = change_data_to_dict(current_data_df)
    request.session['original_form_data'] = dict_with_data_from_form
    request.session['original_form_pk'] = pk_mrl
    request.session['original_form_date'] = request.POST['date_of_read']
    param_value = request.GET.get('image')
    if param_value is not None:
        request.session['original_form_image'] = request.FILES['image']


def chack_data_from_xlsx(data, pk) -> pd.DataFrame:
    """Zadaniem funkcji jest porownanie wjescowego pliku xlsx z danymi ktore zostaly zapisane w bnazie danych"""
    data_in_db = MeterReading.objects.filter(reading_name_id=pk, energy_meter_id__in=EnergyMeters.objects.filter(
        is_add_manual=False)).values('energy_meter', 'meter_reading')
    df_from_data_in_db = pd.DataFrame(data_in_db)
    em_df = modificate_energy_meters_dict()
    df_from_data_in_db = pd.merge(df_from_data_in_db, em_df, how='left', left_on='energy_meter', right_on='id')
    check_data = pd.merge(data, df_from_data_in_db, on='name', how='left', suffixes=('_orginalny', '_w_bazie_danych'))
    check_data.drop(columns=['id', 'is_good'], inplace=True)
    check_data['meter_reading_orginalny'].fillna(0, inplace=True)
    check_data['meter_reading_w_bazie_danych'].fillna(0, inplace=True)
    check_data['diffrent'] = check_data['meter_reading_orginalny'] - check_data['meter_reading_w_bazie_danych']
    check_data['diffrent'] = check_data['diffrent'].astype(int)
    diffrent = check_data.loc[(check_data['diffrent'] > 0) | (check_data['diffrent'] < 0)]
    return diffrent


def data_from_xlx(data, pk) -> str:
    """Funckja ddczytuje dane z xlsx i zapisuje je w bazie danych, a nastepnie sprawdza, czy wszystkie przeslane dane
    zostaly zaimportowane do bazy danych"""
    xlsx_data = pd.read_excel(data)
    good_data_current = xlsx_data[['Unnamed: 1', 'Unnamed: 10']]
    good_data_current = good_data_current.drop(good_data_current.index[:10])
    good_data_current.rename(columns={'Unnamed: 1': 'name', 'Unnamed: 10': 'meter_reading'}, inplace=True)
    delete_data(pk, False)
    save_data_meter_readings(good_data_current, pk)
    not_imported = chack_data_from_xlsx(good_data_current, pk)
    a = 4
