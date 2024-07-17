# Generated by Django 5.0.2 on 2024-07-17 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("electricity_cost", "0036_invoices_type_of_invoice_alter_typeofinvoice_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="energymeters",
            name="conversion_factor",
            field=models.FloatField(default=1, verbose_name="Przelicznik"),
            preserve_default=False,
        ),
    ]