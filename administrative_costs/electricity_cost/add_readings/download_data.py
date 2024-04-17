from ...models import MeterReadingsList
from typing import List
def download_data_to_edit_manual_meter_readings(pk) -> [List, List]:
    """Funkcja ktorej zadanie jest zwrocenie dwoch list zawierajacych dane na temat podanego odczytu.
    Listy te zostana wykorzystane do wygenerowania """