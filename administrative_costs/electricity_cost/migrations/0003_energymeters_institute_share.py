# Generated by Django 5.0.2 on 2024-03-03 21:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "electricity_cost",
            "0002_alter_invoices_cost_alter_invoices_cost_per_1_mwh_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="energymeters",
            name="institute_share",
            field=models.FloatField(blank=True, null=True),
        ),
    ]
