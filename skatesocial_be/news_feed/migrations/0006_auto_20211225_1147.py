# Generated by Django 3.1.7 on 2021-12-25 11:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("news_feed", "0005_remove_event_privacy"),
    ]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="start_at",
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
