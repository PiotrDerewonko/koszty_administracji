# Generated by Django 5.0.2 on 2024-04-29 15:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("electricity_cost", "0028_alter_meterreadingslist_unique_together"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="meterreadingslist", unique_together=set(),
        ),
    ]
