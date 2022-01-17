# Generated by Django 4.0.1 on 2022-01-17 13:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("crew_network", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
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
                ("text", models.CharField(blank=True, max_length=250, null=True)),
                ("start_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("end_at", models.DateTimeField(blank=True, null=True)),
                (
                    "wheel_type",
                    models.CharField(
                        blank=True,
                        choices=[("B", "B"), ("R", "R"), ("I", "I"), ("C", "C")],
                        max_length=1,
                        null=True,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "hidden_from_crews",
                    models.ManyToManyField(
                        related_name="events_hidden", to="crew_network.Crew"
                    ),
                ),
                (
                    "hidden_from_friends",
                    models.ManyToManyField(
                        related_name="events_hidden", to=settings.AUTH_USER_MODEL
                    ),
                ),
                (
                    "spot",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="skate_spots.spot",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "visible_to_crews",
                    models.ManyToManyField(
                        help_text="If supplied, it will be visible to *only* these friends/crews, not any and all friends",
                        related_name="events_visible",
                        to="crew_network.Crew",
                    ),
                ),
                (
                    "visible_to_friends",
                    models.ManyToManyField(
                        help_text="If supplied, it will be visible to *only* these friends/crews, not any and all friends",
                        related_name="events_visible",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ("created_at", "user"),
            },
        ),
        migrations.CreateModel(
            name="EventResponse",
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
                (
                    "rsvp",
                    models.CharField(
                        blank=True,
                        choices=[("G", "Going"), ("N", "Not Going"), ("M", "Maybe")],
                        max_length=1,
                        null=True,
                    ),
                ),
                (
                    "event",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="news_feed.event",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ("event", "user"),
            },
        ),
    ]
