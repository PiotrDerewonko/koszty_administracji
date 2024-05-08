# Generated by Django 5.0.2 on 2024-05-08 13:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("electricity_cost", "0033_alter_meterreadingslist_photo_and_more"),
    ]

    operations = [
        migrations.RemoveField(model_name="counterusage", name="biling_month",),
        migrations.RemoveField(model_name="counterusage", name="biling_year",),
        migrations.AddField(
            model_name="counterusage",
            name="reading_name",
            field=models.ForeignKey(
                default=109,
                on_delete=django.db.models.deletion.PROTECT,
                to="electricity_cost.meterreadingslist",
                verbose_name="Nazwa odczytu",
            ),
            preserve_default=False,
        ),
    ]