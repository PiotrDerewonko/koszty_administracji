from django.db import models
from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist


class Invoices(models.Model):
    invoices_number = models.CharField(verbose_name='Numer faktury', max_length=250)
    cost = models.FloatField(verbose_name='Koszt z faktury')
    cost_per_1_mwh = models.FloatField(verbose_name='Koszt za 1 MWH', null=True, blank=True)
    numbers_mwh = models.FloatField(verbose_name='Ilość zużytych MWH')
    energysuppliers = models.ForeignKey('EnergySuppliers', on_delete=models.PROTECT,
                                        verbose_name='Dostawca')
    biling_month = models.ForeignKey('Month', verbose_name='Miesiąc rozliczeniowy', on_delete=models.PROTECT)
    biling_year = models.ForeignKey('Year', verbose_name='Rok rozliczeniowy', on_delete=models.PROTECT)
    type_of_invoice = models.ForeignKey('TypeOfInvoice', on_delete=models.PROTECT, verbose_name='Typ faktury')
    vat_rate = models.ForeignKey('VatRate', on_delete=models.PROTECT, verbose_name='Stawka Vat', default=1)

    def __str__(self):
        return self.invoices_number


class EnergySuppliers(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class MeterLocations(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class MeterShares(models.Model):
    value = models.FloatField()

    def __str__(self):
        return str(self.value)


class EnergyMeters(models.Model):
    name = models.CharField(max_length=250, verbose_name='Nazwa licznika')
    technical_name = models.CharField(max_length=200, verbose_name='Nazwa licznika z BMS')
    meter_location = models.ForeignKey('MeterLocations', on_delete=models.PROTECT, verbose_name='Lokalizacja licznika')
    museum_share = models.ForeignKey('MeterShares', on_delete=models.PROTECT, related_name='museum_share', default=6,
                                     verbose_name='Udział Muzeum')
    cob_share = models.ForeignKey('MeterShares', on_delete=models.PROTECT, related_name='cob_share', default=6,
                                  verbose_name='Udział COB')
    parish_share = models.ForeignKey('MeterShares', on_delete=models.PROTECT, related_name='parish_share', default=6,
                                     verbose_name='Udział Parafii')
    institute_share = models.ForeignKey('MeterShares', on_delete=models.PROTECT, related_name='institute_share',
                                        default=6, verbose_name='Udział Instytutu')
    is_add_manual = models.BooleanField(default=False, verbose_name='Licznik dodawany ręcznie')
    conversion_factor = models.FloatField(verbose_name='Przelicznik', default=1.00)
    is_virtual = models.BooleanField(verbose_name='Czy wirtualny', default=False)
    initial_value = models.FloatField(verbose_name='Wartość początkowa', default=0)

    def clean(self):

        if float(self.museum_share.value) + float(self.cob_share.value) + float(self.parish_share.value) + float(
                self.institute_share.value) != 1:
            if (self.museum_share_id == 1 or self.cob_share_id == 1 or self.parish_share_id == 1
                    or self.institute_share_id == 1):
                if float(self.museum_share.value) + float(self.cob_share.value) + float(
                        self.parish_share.value) + float(self.institute_share.value) != 0.9999:
                    raise ValidationError('Suma liczników musi być równa 1')
            else:
                raise ValidationError('Suma liczników musi być równa 1')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class FinancialEntity(models.Model):
    name = models.CharField(max_length=250, verbose_name='Nazwa podmiotu')

    def __str__(self):
        return self.name


class Month(models.Model):
    name = models.CharField(max_length=250, verbose_name='Miesiąc')
    number_of_month = models.IntegerField()

    def __str__(self):
        return self.name


class Year(models.Model):
    name = models.CharField(max_length=250, verbose_name='Rok')

    def __str__(self):
        return self.name


class TypeOfInvoice(models.Model):
    """Model odpowiedzialny za słownik typów faktur. Na początku występować będą tylko dwa typpy tzn
    za energie i za przesyl"""
    name = models.CharField(max_length=250, verbose_name='Typ faktury')

    def __str__(self):
        return self.name


class MeterReading(models.Model):
    energy_meter = models.ForeignKey('EnergyMeters', on_delete=models.PROTECT, verbose_name='Licznik')
    meter_reading = models.FloatField(verbose_name='Odczyt licznika')
    reading_name = models.ForeignKey('MeterReadingsList', on_delete=models.PROTECT, verbose_name='Nazwa odczytu')

    def __str__(self):
        return f'''Odczyt licznika {self.energy_meter} z odczytu {self.reading_name}'''


class CounterUsage(models.Model):
    """Model ktory reprezentuje jaki bylo zuzcyie danego licznika  w danym miesiacu i roku rozliczeniowym.
    Celem modelu jest odziolowanie odczytow licznika od zuzycia, zwlaszcz przy edycji danych.
    Poczas edycji danych bedzie uruchamiany osobny skrypt ktory saksuje z tego modelu zuzycie dla edytowanego miesiaca i
    roku oraz kolejnego, a nastwpnie doda dane na nowo. Przy dodwaniu nowoych danych wspomnialy sktrp
    nie bedzie uruchamiany"""
    energy_meter = models.ForeignKey('EnergyMeters', on_delete=models.PROTECT, verbose_name='Licznik')
    usage = models.FloatField(verbose_name='Zużycie licznika')
    reading_name = models.ForeignKey('MeterReadingsList', on_delete=models.PROTECT, verbose_name='Nazwa odczytu')
    usage_institute = models.FloatField(verbose_name='Zużycie instytutu')
    usage_museum = models.FloatField(verbose_name='Zużycie muzeum')
    usage_cob = models.FloatField(verbose_name='Zużycie COB')
    usage_parish = models.FloatField(verbose_name='Zużycie parafii')

    def __str__(self):
        return f'''Zużycie licznika z w wysokości {self.usage}'''


class EnergyMeterTree(models.Model):
    energy_meter_main = models.ForeignKey('EnergyMeters', on_delete=models.PROTECT, related_name='energy_meter_main',
                                          verbose_name='Licznik nadrzędny')
    energy_meter_submain = models.ForeignKey('EnergyMeters', on_delete=models.PROTECT,
                                             related_name='energy_meter_submain',
                                             verbose_name='Licznik poddrzędny')

    def __str__(self):
        return f'''Licznik nadrzędny {self.energy_meter_main} w {self.energy_meter_submain}'''


class MeterReadingsList(models.Model):
    """Model w ktorym okreslamy, nazwe robocza odczytu oraz miesiac i rok obrachunnkowy. Model ma dwa zadania:
    1) nie dopusici do sytuacji, gdzie ktos doda np recznie dwa razy te same dane, np liczniki spisywane recznie
    2) latwe wyszukiwanie w tabeli z odczytami, odczytow dotyczacych danego roku i miesiaca"""
    biling_month = models.ForeignKey('Month', verbose_name='Miesiąc rozliczeniowy', on_delete=models.PROTECT)
    biling_year = models.ForeignKey('Year', verbose_name='Rok rozliczeniowy', on_delete=models.PROTECT)
    date_of_read = models.DateField(verbose_name='Data odczytu', auto_now=False, auto_now_add=False, null=True,
                                    blank=True)
    photo = models.FileField(verbose_name='Zdjecie licznika', upload_to='files/%Y/%m/%d', null=True, blank=True)
    xlsx_file = models.FileField(verbose_name='Dane z odczytu automatycznego', upload_to='files_xlsx/%Y/%m/%d',
                                 null=True, blank=True)
    add_manualy = models.BooleanField(default=False)
    add_automatic = models.BooleanField(default=False)

    def clean(self):
        all_readings = MeterReading.objects.all()
        if len(all_readings) > 0:
            current_year = self.biling_year.id
            current_month = self.biling_month.id
            try:
                previous_month = current_month - 1
                previous_year = current_year
                if previous_month == 0:
                    previous_month = 12
                    previous_year -= 1
                MeterReadingsList.objects.get(biling_month=previous_month, biling_year=previous_year)
            except ObjectDoesNotExist:
                raise ValidationError('Nie ma poprzedniego okresu')

    class Meta:
        unique_together = ['biling_month', 'biling_year']

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Odczyt za rok: {self.biling_year} oraz miesiac {self.biling_month}'


class VatRate(models.Model):
    """Model który przechowuje wysokości stawek VAT."""
    name = models.IntegerField(verbose_name='Stawka vat')

    def __str__(self):
        return f'{self.name} %'


class MeterReadingHistory(models.Model):
    """Model który przechowuje historie zmian dokonane przez uztkownika w zakresie odczytow licznika"""
    energy_meter = models.FloatField(verbose_name='Licznik')
    meter_reading = models.FloatField(verbose_name='Odczyt licznika')
    reading_name = models.FloatField(verbose_name='Lista licznika')
    user = models.CharField(verbose_name='Nazwa użytkownika')
    data_of_changed = models.DateField(verbose_name='Data zmiany')
