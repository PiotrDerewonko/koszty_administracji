# forms.py

from django import forms
from .models import EnergyMeters, Month, Year
from django.core.validators import FileExtensionValidator


def get_energy_meter_form(energy_meters_fields):
    fields = {
        'year': forms.ModelChoiceField(queryset=Year.objects.all(), label='Rok Rozliczeniowy', required=True,
                                       widget=forms.Select(attrs={'class': 'inline-field'})),
        'month': forms.ModelChoiceField(queryset=Month.objects.all(), label='Miesiąc Rozliczeniowy', required=True,
                                        widget=forms.Select(attrs={'class': 'inline-field'})),
        'date_of_read': forms.DateField(label='Data odczytu', required=True,
                                        widget=forms.DateInput(attrs={'type': 'date'})),
        'image': forms.FileField(label='Dodaj jeden plik ze zdjęciami', required=False
                                 , validators=[
                FileExtensionValidator(allowed_extensions=['zip', 'rar', 'tar', 'tar.gz', 'tar'])]),

    }

    for field in energy_meters_fields:
        field_name = field.name
        fields[field_name] = forms.FloatField(required=True)

    return type('EnergyMeterForm', (forms.Form,), fields)
