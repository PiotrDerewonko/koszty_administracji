# Generated by Django 5.0.2 on 2024-11-04 09:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("electricity_cost", "0044_invoices_vat_rate"),
    ]

    operations = [
        migrations.AlterField(
            model_name="invoices",
            name="vat_rate",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.PROTECT,
                to="electricity_cost.vatrate",
                verbose_name="Stawka Vat",
            ),
        ),
    ]
