from django.db import models
from django.core.exceptions import ValidationError


class Invoices(models.Model):
    invoices_number = models.FloatField(verbose_name='Numer faktury')
    cost = models.FloatField(verbose_name='Koszt z faktury')
    cost_per_1_mwh = models.FloatField(verbose_name='Koszt za 1 MWH')
    numbers_mwh = models.FloatField(verbose_name='Ilość zużytych MWH')
    energysuppliers = models.ForeignKey('EnergySuppliers', on_delete=models.CASCADE,
                                        verbose_name='Dostawca')
    #todo potwierdzic nazwy kolumn
    month = models.IntegerField(verbose_name='Miesiąc zużycia')
    year = models.IntegerField(verbose_name='Rok zużycia')


class EnergySuppliers(models.Model):
    name = models.TextField(max_length=100)

    def __str__(self):
        return self.name


class MeterLocations(models.Model):
    name = models.TextField(max_length=200)

    def __str__(self):
        return self.name


class EnergyMeters(models.Model):
    name = models.TextField(max_length=200, verbose_name='Nazwa licznika')
    technical_name = models.TextField(max_length=200, verbose_name='Nazwa licznika z BMS')
    meter_location = models.ForeignKey('MeterLocations', on_delete=models.CASCADE, verbose_name='Lokalizacja licznika')
    museum_share = models.FloatField(default=0, verbose_name='Udział Muzeum')
    cob_share = models.FloatField(default=0, verbose_name='Udział COB')
    parish_share = models.FloatField(default=0, verbose_name='Udział Parafii')
    institute_share = models.FloatField(default=0, verbose_name='Udział Instytutu')

    def clean(self):
        if self.museum_share + self.cob_share + self.parish_share + self.institute_share != 1:
            raise ValidationError('Suma liczników musi być równa 1')
