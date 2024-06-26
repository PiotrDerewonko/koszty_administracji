from ..models import MeterReadingsList, MeterReading, EnergyMeters
from typing import List, Iterable


def download_data_to_edit_manual_meter_readings(pk, is_add_manual) -> [List, Iterable[MeterReading]]:
    """Funkcja ktorej zadanie jest zwrocenie listy oraz słownika zawierajacych dane na temat podanego odczytu.
    Dane te zostana wykorzystane do wygenerowania formularza edycji danego odczytu. """

    # pobieram stale dane dla odczytu
    data_static = []
    data_mrl = MeterReadingsList.objects.get(pk=pk)
    data_static.append(data_mrl.biling_year_id)
    data_static.append(data_mrl.biling_month_id)
    data_static.append(data_mrl.date_of_read)
    data_static.append(data_mrl.photo)

    # pobieram dane dotyczace poszczegolnych licznikow
    data_mr = MeterReading.objects.filter(reading_name_id=pk,
                                          energy_meter_id__in=EnergyMeters.objects.filter(is_add_manual=is_add_manual))

    return data_static, data_mr
