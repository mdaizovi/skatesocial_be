# Generated by Django 3.1.7 on 2021-12-22 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("skate_spots", "0002_auto_20211222_1809"),
    ]

    operations = [
        migrations.AddField(
            model_name="spot",
            name="private",
            field=models.BooleanField(default=False),
        ),
    ]
