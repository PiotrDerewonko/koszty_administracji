from django.contrib import admin
from .models import EnergyMeters, EnergySuppliers, Invoices, MeterLocations


class InvoicesAdmin(admin.ModelAdmin):
    list_display = ['invoices_number', 'cost', 'cost_per_1_mwh', 'numbers_mwh', 'energysuppliers']


admin.site.register(Invoices, InvoicesAdmin)
admin.site.register(MeterLocations)
admin.site.register(EnergySuppliers)
admin.site.register(EnergyMeters)
