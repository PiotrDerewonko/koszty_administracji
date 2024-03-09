from django.db import models
from django.core.exceptions import ValidationError


class Invoices(models.Model):
    invoices_number = models.CharField(verbose_name='Numer faktury', max_length=250)
    cost = models.FloatField(verbose_name='Koszt z faktury')
    cost_per_1_mwh = models.FloatField(verbose_name='Koszt za 1 MWH')
    numbers_mwh = models.FloatField(verbose_name='Ilość zużytych MWH')
    energysuppliers = models.ForeignKey('EnergySuppliers', on_delete=models.PROTECT,
                                        verbose_name='Dostawca')
    biling_month = models.IntegerField(verbose_name='Miesiąc rozliczeniowy')
    biling_year = models.IntegerField(verbose_name='Rok rozliczeniowy')

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

    def clean(self):

        if float(self.museum_share.value) + float(self.cob_share.value) + float(self.parish_share.value) + int(
                self.institute_share.value) != 1:
            if self.museum_share_id == 1 or self.cob_share_id == 1 or self.parish_share_id == 1 or self.institute_share_id == 1:
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


class MeterReading(models.Model):
    energy_meter = models.ForeignKey('EnergyMeters', on_delete=models.CASCADE, verbose_name='Licznik')
    date_of_reading = models.DateField(verbose_name='Data odczytu')
    meter_reading = models.FloatField(verbose_name='Odczyt licznika')
    biling_month = models.ForeignKey('Month', verbose_name='Miesiąc rozliczeniowy', on_delete=models.PROTECT)
    biling_year = models.ForeignKey('Year', verbose_name='Rok rozliczeniowy', on_delete=models.PROTECT)

    def __str__(self):
        return f'''Odczyt licznika {self.energy_meter} z dnia {self.date_of_reading}'''
