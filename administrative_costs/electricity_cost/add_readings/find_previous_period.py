from typing import List

import pandas as pd

from ..models import MeterReadingsList, MeterReading, EnergyMeters
from django.core.exceptions import ObjectDoesNotExist

def find_previous_period(year: int, month: int) -> [int, int]:
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


