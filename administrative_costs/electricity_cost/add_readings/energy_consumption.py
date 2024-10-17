import pandas as pd
from ..models import CounterUsage, MeterReadingsList, EnergyMeters, EnergyMeterTree
from ..add_readings.find_previous_period import find_previous_period, find_period_data
import json


def delete_energy_consumption(year, month) -> None:
    """Funkcja ktora kasuje zuzycie licnzikow za dany miesiac i rok obrachunkowy"""
    mrl_pk = MeterReadingsList.objects.filter(biling_year=year, biling_month=month)
    mrl_id = mrl_pk[0].id
    to_delete = CounterUsage.objects.filter(reading_name=mrl_id)
    to_delete.delete()


def add_energy_consumption(year: int, month: int) -> None:
    """funkcja ktora dodaje dla kazdego licznika jego zuzycie, porownujac dane przekazane w
    wpisywanym miesiacu z danymi za miesiac poprzedni. """
    delete_energy_consumption(year, month)
    mrl_pk = MeterReadingsList.objects.filter(biling_year=year, biling_month=month)
    mrl_id = mrl_pk[0].id
    energy_meters_query = EnergyMeters.objects.select_related('museum_share', 'cob_share', 'parish_share',
                                                              'institute_share')
    #todo dodac tutaj odczyt poczatkowy licznika i odejmowac go od obu wartosci
    data = []
    for meter in energy_meters_query:
        data.append({
            'id': meter.id,
            'museum_share': meter.museum_share.value,
            'cob_share': meter.cob_share.value,
            'parish_share': meter.parish_share.value,
            'institute_share': meter.institute_share.value,
            'conversion_factor': meter.conversion_factor
        })

    # Tworzenie DataFrame
    energy_meters = pd.DataFrame(data)
    previous_year, previous_month = find_previous_period(year, month)
    query_previous_month = find_period_data(previous_year, previous_month)
    query_current_month = find_period_data(year, month)
    data_previous_df = pd.DataFrame.from_dict(query_previous_month)
    data_current_df = pd.DataFrame.from_dict(query_current_month)
    if len(data_previous_df) > 0:
        compared_data = pd.merge(data_current_df, data_previous_df, how='left', on='energy_meter_id',
                                 suffixes=('_current', '_previous'))
        compared_data.fillna(0, inplace=True)
        compared_data['difference'] = 0
        compared_data['difference'] = compared_data['meter_reading_current'] - compared_data['meter_reading_previous']
        data_to_save = compared_data[['energy_meter_id', 'difference']]
    else:
        data_to_save = data_current_df[['energy_meter_id', 'meter_reading']]
        data_to_save = data_to_save.rename(columns={'meter_reading': 'difference'})
    # dodaje przeliczniki dla kazdego licznika i przeliczam ile wyniosla dla kazdej instytucji zuzycie
    data_to_save = pd.merge(data_to_save, energy_meters[
        ['id', 'museum_share', 'cob_share', 'parish_share', 'institute_share', 'conversion_factor']], how='left',
                            left_on='energy_meter_id', right_on='id')
    data_to_save['difference'] = data_to_save['difference'] * data_to_save['conversion_factor']
    data_to_save[['usage_institute', 'usage_museum', 'usage_cob', 'usage_parish']] = 0, 0, 0, 0
    data_to_save['usage_institute'] = data_to_save['difference'] * data_to_save['institute_share']
    data_to_save['usage_parish'] = data_to_save['difference'] * data_to_save['parish_share']
    data_to_save['usage_cob'] = data_to_save['difference'] * data_to_save['cob_share']
    data_to_save['usage_museum'] = data_to_save['difference'] * data_to_save['museum_share']

    data_to_save = add_virtual_energy_consumption(data_to_save, month)

    # zapis danych
    save_data(data_to_save, mrl_id)


def add_virtual_energy_consumption(data, mrl_id) -> pd.DataFrame:
    energy_meters_query = EnergyMeters.objects.filter(is_virtual=True)
    data_tmp_level_high = pd.DataFrame(
        columns=['energy_meter_id', 'difference', 'reading_name_id', 'usage_museum', 'usage_cob', 'usage_parish',
                 'usage_institute'])
    for meter in energy_meters_query:
        meter_id = meter.id
        data_tmp = pd.DataFrame(
            columns=['energy_meter_id', 'difference', 'reading_name_id', 'usage_museum', 'usage_cob', 'usage_parish',
                     'usage_institute'])
        sub_meter_id = EnergyMeterTree.objects.filter(energy_meter_main=meter_id).values()
        for sub in sub_meter_id:
            data_tmp_submain = pd.DataFrame(columns=['energy_meter_id'], index=[0])
            sub_id = sub['energy_meter_submain_id']
            data_tmp_submain['energy_meter_id'] = meter_id
            try:
                data_tmp_submain['difference'] = data['difference'].loc[data['energy_meter_id'] == sub_id].iloc[0]
                data_tmp_submain['usage_museum'] = data['usage_museum'].loc[data['energy_meter_id'] == sub_id].iloc[0]
                data_tmp_submain['usage_cob'] = data['usage_cob'].loc[data['energy_meter_id'] == sub_id].iloc[0]
                data_tmp_submain['usage_parish'] = data['usage_parish'].loc[data['energy_meter_id'] == sub_id].iloc[0]
                data_tmp_submain['usage_institute'] = \
                data['usage_institute'].loc[data['energy_meter_id'] == sub_id].iloc[0]
                data_tmp = pd.concat([data_tmp, data_tmp_submain], ignore_index=True)
            except IndexError:
                print(f'Nie ma danych podlicznikow dla licznika o id {sub_id}')
        try:
            data_tmp[['difference', 'usage_museum', 'usage_cob', 'usage_parish', 'usage_institute']] = (
                data_tmp)[['difference', 'usage_museum', 'usage_cob', 'usage_parish', 'usage_institute']].cumsum()
            data_tmp = data_tmp.iloc[-1].to_frame().transpose()
            data_tmp_level_high = pd.concat([data_tmp_level_high, data_tmp], ignore_index=True)
            print(f'dodano dane zuzcyie do wirtualnego licznika o id {meter_id}')
        except IndexError:
            print(f'Nie dodano wirtualnego odczytu dla licznika o id {meter_id}')
    data_to_return = pd.concat([data, data_tmp_level_high], ignore_index=True)
    return data_to_return


def save_data(data: pd.DataFrame, mrl_id) -> None:
    '''funckja zapisuje przekazyny dataframe do bazy danych, wczesniej zamieniajac go na json.'''
    # zapisuje dane do bazy danych
    data['reading_name_id'] = mrl_id
    data_to_save_json = data.to_json(orient='records')
    data_to_save_json = json.loads(data_to_save_json)
    for item in data_to_save_json:
        CounterUsage.objects.create(
            usage=item['difference'],
            energy_meter_id=item['energy_meter_id'],
            reading_name_id=item['reading_name_id'],
            usage_museum=item['usage_museum'],
            usage_cob=item['usage_cob'],
            usage_parish=item['usage_parish'],
            usage_institute=item['usage_institute']
        )
