# Generated by Django 5.0.2 on 2024-03-03 21:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="EnergySuppliers",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.TextField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="MeterLocations",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.TextField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name="Invoices",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("invoices_number", models.FloatField()),
                ("cost", models.FloatField()),
                ("cost_per_1_mwh", models.FloatField()),
                ("numbers_mwh", models.FloatField()),
                (
                    "energysuppliers",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="electricity_cost.energysuppliers",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="EnergyMeters",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.TextField(max_length=200)),
                ("museum_share", models.FloatField()),
                ("cob_share", models.FloatField()),
                ("parish_share", models.FloatField()),
                (
                    "meter_location",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="electricity_cost.meterlocations",
                    ),
                ),
            ],
        ),
    ]
