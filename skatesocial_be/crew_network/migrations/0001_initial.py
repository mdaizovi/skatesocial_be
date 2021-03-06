# Generated by Django 4.0.1 on 2022-01-17 13:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Friendship",
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
                ("users", models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name="FriendRequest",
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
                ("initiated_at", models.DateTimeField(auto_now_add=True)),
                (
                    "initiated_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="initiated_friend_requests",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "target",
                    models.ForeignKey(
                        help_text="user initiated wants to connect with",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="pending_friend_requests",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Crew",
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
                ("name", models.CharField(max_length=100)),
                (
                    "members",
                    models.ManyToManyField(
                        related_name="crews_included", to=settings.AUTH_USER_MODEL
                    ),
                ),
                (
                    "owned_by",
                    models.ForeignKey(
                        help_text="User that made this crew, for their provacy reasons",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="crews_owned",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
