# Generated by Django 5.0.2 on 2024-03-19 21:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("electricity_cost", "0018_remove_counterusage_biling_month_and_more"),
    ]

    operations = [
        migrations.RemoveField(model_name="meterreading", name="biling_month",),
        migrations.RemoveField(model_name="meterreading", name="biling_year",),
        migrations.AddField(
            model_name="counterusage",
            name="biling_month",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.PROTECT,
                to="electricity_cost.month",
                verbose_name="Miesiąc rozliczeniowy",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="counterusage",
            name="biling_year",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.PROTECT,
                to="electricity_cost.year",
                verbose_name="Rok rozliczeniowy",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="meterreading",
            name="reading_name",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.PROTECT,
                to="electricity_cost.meterreadingslist",
                verbose_name="Nazwa odczytu",
            ),
            preserve_default=False,
        ),
    ]
