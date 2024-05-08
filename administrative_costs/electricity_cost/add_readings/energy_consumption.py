import pandas as pd
from ..models import CounterUsage, MeterReadingsList
from ..add_readings.find_previous_period import find_previous_period, find_period_data
from ..add_readings.modificate_data import change_form_to_df
import json

def delete_energy_consumption(year, month) -> None:
    """Funkcja ktora kasuje zuzycie licnzikow za dany miesiac i rok obrachunkowy"""
    mrl_pk = MeterReadingsList.objects.filter(biling_year=year, biling_month=month)
    id = mrl_pk[0].id
    to_delete = CounterUsage.objects.filter(reading_name=id)
    to_delete.delete()


def add_energy_consumption(year: int, month: int) -> None:
    """funkcja ktora dodaje dla kazdego licznika jego zuzycie, porownujac dane przekazane w
    wpisywanym miesiacu z danymi za miesiac poprzedni. """
    delete_energy_consumption(year, month)
    mrl_pk = MeterReadingsList.objects.filter(biling_year=year, biling_month=month)
    id = mrl_pk[0].id
    previous_year, previous_month = find_previous_period(year, month)

    query_previous_month = find_period_data(previous_year, previous_month)
    query_current_month = find_period_data(year, month)
    data_previous_df = pd.DataFrame.from_dict(query_previous_month)
    data_current_df = pd.DataFrame.from_dict(query_current_month)
    compared_data = pd.merge(data_current_df, data_previous_df, how='left', on='energy_meter_id',
                             suffixes=('_current', '_previous'))
    compared_data.fillna(0, inplace=True)
    compared_data['difference'] = 0
    compared_data['difference'] = compared_data['meter_reading_current'] - compared_data['meter_reading_previous']
    data_to_save = compared_data[['energy_meter_id', 'difference']]
    data_to_save['reading_name_id'] = id
    data_to_save_json = data_to_save.to_json(orient='records')
    data_to_save_json = json.loads(data_to_save_json)
    for item in data_to_save_json:
        CounterUsage.objects.create(
            usage=item['difference'],
            energy_meter_id=item['energy_meter_id'],
            reading_name_id=item['reading_name_id']
        )
