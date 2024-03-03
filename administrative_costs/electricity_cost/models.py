from django.db import models
from django.core.exceptions import ValidationError


class Invoices(models.Model):
    invoices_number = models.FloatField(verbose_name='Numer faktury')
    cost = models.FloatField(verbose_name='Koszt z faktury')
    cost_per_1_mwh = models.FloatField(verbose_name='Koszt za 1 MWH')
    numbers_mwh = models.FloatField(verbose_name='Ilość zużytych MWH')
    energysuppliers = models.ForeignKey('EnergySuppliers', on_delete=models.CASCADE,
                                        verbose_name='Dostawca')


class EnergySuppliers(models.Model):
    name = models.TextField(max_length=100)

    def __str__(self):
        return self.name


class MeterLocations(models.Model):
    name = models.TextField(max_length=200)


class EnergyMeters(models.Model):
    name = models.TextField(max_length=200)
    meter_location = models.ForeignKey('MeterLocations', on_delete=models.CASCADE)
    museum_share = models.FloatField()
    cob_share = models.FloatField()
    parish_share = models.FloatField()

    def clean(self):
        if self.museum_share + self.cob_share + self.parish_share != 1:
            raise ValidationError('Suma liczników musi być równa 1')
