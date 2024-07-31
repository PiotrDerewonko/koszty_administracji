from django.test import TestCase
from ..models import EnergyMeters, MeterShares, MeterLocations, Month, Year, Invoices, EnergySuppliers, TypeOfInvoice
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


class InvoicesTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Month.objects.create(name='styczen', number_of_month=1)
        Year.objects.create(name=2024)
        EnergySuppliers.objects.create(name='PGE')
        TypeOfInvoice.objects.create(name='test')

    def setUp(self):
        Invoices.objects.create(invoices_number='Testowa Faktura', cost=1, cost_per_1_mwh=1, numbers_mwh=1,
                                energysuppliers_id=1,
                                biling_month_id=1, biling_year_id=1, type_of_invoice_id=1)

    def test_create_invoice(self):
        i1 = Invoices.objects.get(pk=1)
        self.assertEqual(str(i1), 'Testowa Faktura')
        self.assertEqual(i1.cost, 1)


class TestTypyInvoices(TestCase):
    def setUp(self):
        TypeOfInvoice.objects.create(name='Testowy typ')

    def test_create_type_of_invoice(self):
        i1 = TypeOfInvoice.objects.get(pk=1)
        self.assertEqual(str(i1), 'Testowy typ')
