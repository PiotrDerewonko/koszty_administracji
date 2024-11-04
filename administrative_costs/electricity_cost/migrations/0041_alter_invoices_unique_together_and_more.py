# Generated by Django 5.0.2 on 2024-10-16 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("electricity_cost", "0040_alter_meterreadingslist_date_of_read"),
    ]

    operations = [
        migrations.AlterUniqueTogether(name="invoices", unique_together=set(),),
        migrations.AlterField(
            model_name="invoices",
            name="cost_per_1_mwh",
            field=models.FloatField(
                blank=True, null=True, verbose_name="Koszt za 1 MWH"
            ),
        ),
    ]