from django.contrib import admin
from .models import EnergyMeters, EnergySuppliers, Invoices, MeterLocations


class InvoicesAdmin(admin.ModelAdmin):
    list_display = ['invoices_number', 'cost', 'cost_per_1_mwh', 'numbers_mwh', 'energysuppliers', 'month', 'year']
    list_filter = ['invoices_number', 'month', 'year']
    search_fields = ['invoices_number', 'cost']

class EnergyMetersAdmin(admin.ModelAdmin):
    list_display = ['name', 'meter_location', 'museum_share', 'cob_share', 'parish_share', 'institute_share']

class MeterLocationsAdmin(admin.ModelAdmin):
    list_display = ['name']

class Energy_SuppliersAdmin(admin.ModelAdmin):
    list_display = ['name']


admin.site.register(Invoices, InvoicesAdmin)
admin.site.register(MeterLocations, MeterLocationsAdmin)
admin.site.register(EnergySuppliers, Energy_SuppliersAdmin)
admin.site.register(EnergyMeters, EnergyMetersAdmin)
