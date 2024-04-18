# forms.py

from django import forms
from .models import EnergyMeters, Month, Year
from django.core.validators import FileExtensionValidator


def get_energy_meter_form(energy_meters_fields, data_static=None, data_dynamic=None):
    fields = {
        'year': forms.ModelChoiceField(queryset=Year.objects.all(), label='Rok Rozliczeniowy', required=True,
                                       widget=forms.Select(attrs={'class': 'inline-field'}),
                                       initial=data_static[0] if data_static else None),
        'month': forms.ModelChoiceField(queryset=Month.objects.all(), label='Miesiąc Rozliczeniowy', required=True,
                                        widget=forms.Select(attrs={'class': 'inline-field'}),
                                        initial=data_static[1] if data_static else None),
        'date_of_read': forms.DateField(label='Data odczytu', required=True,
                                        widget=forms.DateInput(attrs={'type': 'date'}),
                                        initial=data_static[2] if data_static else None),
        'image': forms.FileField(label='Dodaj jeden plik ze zdjęciami', required=False
                                 , validators=[
                FileExtensionValidator(allowed_extensions=['zip', 'rar', 'tar', 'tar.gz', 'tar'])],
                                 initial=data_static[3] if data_static else None),

    }
    if data_dynamic == None:
        for field in energy_meters_fields:
            field_name = field.name
            #todo tu brac ze slownika
            fields[field_name] = forms.FloatField(required=True)
    else:
        for field in data_dynamic:
            field_name = field.energy_meter.name
            fields[field_name] = forms.FloatField(required=True, initial=field.meter_reading)

    return type('EnergyMeterForm', (forms.Form,), fields)
