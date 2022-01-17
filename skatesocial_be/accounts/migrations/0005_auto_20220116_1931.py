# Generated by Django 3.1.7 on 2022-01-16 19:31

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0004_userlocation"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userlocation",
            name="location",
            field=django.contrib.gis.db.models.fields.PointField(
                blank=True, geography=True, null=True, srid=4326
            ),
        ),
    ]
