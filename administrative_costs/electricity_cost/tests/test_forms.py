from django.test import TestCase
from electricity_cost.forms import *
from electricity_cost.models import *


class FormTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        MeterLocations.objects.create(name='Meter')
        MeterShares.objects.create(value=1)
        MeterShares.objects.create(value=0)
        Year.objects.create(name=2023)
        Month.objects.create(name='Styczeń', number_of_month=1)

    def setUp(self):
        EnergyMeters.objects.create(name='Electricity Meter', meter_location_id=1, cob_share_id=1, institute_share_id=2,
                                    museum_share_id=2, parish_share_id=2, technical_name='test')
        MeterReadingsList.objects.create(biling_year_id=1, biling_month_id=1, date_of_read='2023-01-01')
        MeterReading.objects.create(meter_reading=1, energy_meter_id=1, reading_name_id=1)

    def test_good_values(self):
        data = EnergyMeters.objects.all()
        form_class = get_energy_meter_form(data)
        form_instance = form_class(data={'Electricity Meter': 1, 'year': 1, 'month': 1, 'date_of_read': '2023-01-01'})
        a = form_instance.is_valid()
        self.assertTrue(form_instance.is_valid())  #

    def test_minus_values(self):
        data = EnergyMeters.objects.all()
        form_class = get_energy_meter_form(data)
        form_instance = form_class(data={'Electricity Meter': -11, 'year': 1, 'month': 1, 'date_of_read': '2023-01-01'})
        a = form_instance.is_valid()
        self.assertFalse(form_instance.is_valid())  #

    def test_wrong_values(self):
        data = EnergyMeters.objects.all()
        form_class = get_energy_meter_form(data)
        form_instance = form_class(data={'Electricity Meter': 1, 'year': 111, 'month': 11, 'date_of_read': '202-01-01'})
        a = form_instance.is_valid()
        self.assertFalse(form_instance.is_valid())  #
