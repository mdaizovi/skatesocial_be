# Generated by Django 3.1.7 on 2021-12-18 20:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("skate_spots", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Event",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("user", models.URLField()),
                ("text", models.CharField(blank=True, max_length=250, null=True)),
                ("start_at", models.DateTimeField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "privacy",
                    models.CharField(
                        choices=[
                            ("P", "Public"),
                            ("F", "Friends"),
                            ("C", "Crew"),
                            ("E", "Except"),
                        ],
                        default="F",
                        max_length=1,
                    ),
                ),
                (
                    "spot",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="skate_spots.spot",
                    ),
                ),
            ],
        ),
    ]