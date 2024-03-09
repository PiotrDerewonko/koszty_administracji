from django.test import TestCase
from .models import EnergyMeters, MeterShares, MeterLocations
from django.core.exceptions import ValidationError

class EnergyMetersTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        MeterShares.objects.create(value=0.3333)
        MeterShares.objects.create(value=0.5)
        MeterShares.objects.create(value=0.25)
        MeterShares.objects.create(value=0.75)
        MeterShares.objects.create(value=0.1)
        MeterShares.objects.create(value=0)
        MeterLocations.objects.create(name='test')

    def setUp(self):
        EnergyMeters.objects.create(name='Test udzial 0.3333', technical_name='testowa techniczna nazwa',
                                    meter_location_id=1, museum_share_id=1, cob_share_id=1, parish_share_id=6,
                                    institute_share_id=1)

    def test_energy_meters_raises(self):
        with self.assertRaises(ValidationError):
            EnergyMeters.objects.create(name='Test udzial 0.3333', technical_name='testowa techniczna nazwa',
                                        meter_location_id=1, museum_share_id=6, cob_share_id=6, parish_share_id=6,
                                        institute_share_id=6)

    def test_energy_meters_str(self):
        e1 = EnergyMeters.objects.get(pk=1)
        self.assertEqual(str(e1), 'Test udzial 0.3333')



