# Generated by Django 5.0.2 on 2024-04-29 10:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("electricity_cost", "0024_meterreadingslist_xlsx_file"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="invoices",
            unique_together={("biling_month", "biling_year", "energysuppliers")},
        ),
    ]