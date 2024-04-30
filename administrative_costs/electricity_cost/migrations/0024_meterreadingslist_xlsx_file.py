# Generated by Django 5.0.2 on 2024-04-26 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("electricity_cost", "0023_energymeters_is_add_manual"),
    ]

    operations = [
        migrations.AddField(
            model_name="meterreadingslist",
            name="xlsx_file",
            field=models.FileField(
                default='',
                upload_to="files_xlsx/%Y/%m/%d",
                verbose_name="Dane z odczytu automatycznego",
            ),
            preserve_default=False,
        ),
    ]