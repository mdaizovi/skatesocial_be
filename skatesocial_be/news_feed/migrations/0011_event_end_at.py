# Generated by Django 3.1.7 on 2022-01-16 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("news_feed", "0010_event_wheel_type"),
    ]

    operations = [
        migrations.AddField(
            model_name="event",
            name="end_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
