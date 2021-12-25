from datetime import datetime

from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

from .model_choices import EventResponseChoices
from crew_network.models import Crew

User = get_user_model()


class Event(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=250, null=True, blank=True)
    spot = models.ForeignKey("skate_spots.Spot", on_delete=models.CASCADE)
    start_at = models.DateTimeField(default=datetime.now)

    created_at = models.DateTimeField(auto_now_add=True)

    visible_to_friends = models.ManyToManyField(
        User,
        related_name="events_visible",
    )
    visible_to_crews = models.ManyToManyField(
        Crew,
        related_name="events_visible",
    )
    hidden_from_friends = models.ManyToManyField(
        User,
        related_name="events_hidden",
    )
    hidden_from_crews = models.ManyToManyField(
        Crew,
        related_name="events_hidden",
    )

    def __str__(self):
        return "<{}> {}, {}".format(
            self.__class__.__name__,
            self.user,
            self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        )

    def clean(self):
        if (not self.text) and (not self.spot):
            raise ValidationError("Must have either text or a spot")


class EventResponse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    rsvp = models.CharField(
        max_length=1, choices=EventResponseChoices.CHOICES, null=True, blank=True
    )
