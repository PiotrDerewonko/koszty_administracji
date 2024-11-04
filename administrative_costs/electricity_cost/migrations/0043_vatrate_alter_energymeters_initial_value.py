# Generated by Django 5.0.2 on 2024-11-04 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("electricity_cost", "0042_energymeters_initial_value"),
    ]

    operations = [
        migrations.CreateModel(
            name="VatRate",
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
                ("name", models.IntegerField(verbose_name="Stawka vat")),
            ],
        ),
        migrations.AlterField(
            model_name="energymeters",
            name="initial_value",
            field=models.FloatField(default=0, verbose_name="Wartość początkowa"),
        ),
    ]