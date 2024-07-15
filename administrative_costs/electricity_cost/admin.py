from django.contrib import admin
from .models import (EnergyMeters, EnergySuppliers, Invoices, MeterLocations, FinancialEntity, MeterReading, Month,
                     Year, CounterUsage, EnergyMeterTree, MeterReadingsList, TypeOfInvoice)


class InvoicesAdmin(admin.ModelAdmin):
    list_display = ['invoices_number', 'cost', 'cost_per_1_mwh', 'numbers_mwh', 'energysuppliers', 'biling_month',
                    'biling_year']
    list_filter = ['invoices_number', 'biling_month', 'biling_year']
    search_fields = ['invoices_number', 'cost']


class EnergyMetersAdmin(admin.ModelAdmin):
    list_display = ['name', 'meter_location', 'museum_share', 'cob_share', 'parish_share', 'institute_share']
    list_filter = ['name', 'meter_location']
    search_fields = ['name']
    search_help_text = 'Szukaj po nazwie licznika'


class MeterLocationsAdmin(admin.ModelAdmin):
    list_display = ['name']


class EnergySuppliersAdmin(admin.ModelAdmin):
    list_display = ['name']


class MeterReadingAdmin(admin.ModelAdmin):
    list_display = [field.name for field in MeterReading._meta.fields]
    list_filter = ['energy_meter']


class MonthAdmin(admin.ModelAdmin):
    list_display = ['name', 'number_of_month']


class YearAdmin(admin.ModelAdmin):
    list_display = ['name']


class CounterUsageAdmin(admin.ModelAdmin):
    list_display = ['id', 'energy_meter', 'usage', 'reading_name']
    list_filter = ['energy_meter']


class EnergyMeterTreeAdmin(admin.ModelAdmin):
    list_display = ['id', 'energy_meter_main', 'energy_meter_submain']

class MeterReadingListAdmin(admin.ModelAdmin):
    list_display = ['id', 'biling_month', 'biling_year', 'add_manualy', 'add_automatic']

class TypeOfInvoiceAdmin(admin.ModelAdmin):
    list_display = ['name']


admin.site.register(Invoices, InvoicesAdmin)
admin.site.register(MeterLocations, MeterLocationsAdmin)
admin.site.register(EnergySuppliers, EnergySuppliersAdmin)
admin.site.register(EnergyMeters, EnergyMetersAdmin)
admin.site.register(FinancialEntity)
admin.site.register(MeterReading, MeterReadingAdmin)
admin.site.register(Month, MonthAdmin)
admin.site.register(Year, YearAdmin)
admin.site.register(CounterUsage, CounterUsageAdmin)
admin.site.register(EnergyMeterTree, EnergyMeterTreeAdmin)
admin.site.register(MeterReadingsList, MeterReadingListAdmin)
admin.site.register(TypeOfInvoice, TypeOfInvoiceAdmin)
