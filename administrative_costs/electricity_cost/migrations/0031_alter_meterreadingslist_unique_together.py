# Generated by Django 5.0.2 on 2024-04-30 08:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("electricity_cost", "0030_alter_meterreadingslist_unique_together"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="meterreadingslist", unique_together=set(),
        ),
    ]
