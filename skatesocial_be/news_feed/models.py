from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

from .model_choices import PrivacyChoices

User = get_user_model()


class Event(models.Model):
    user = models.URLField()
    text = models.CharField(max_length=250, null=True, blank=True)
    spot = models.ForeignKey(
        "skate_spots.Spot", null=True, blank=True, on_delete=models.SET_NULL
    )
    start_at = models.DateTimeField()

    created_at = models.DateTimeField(auto_now_add=True)
    privacy = models.CharField(
        max_length=1,
        choices=PrivacyChoices.CHOICES,
        default=PrivacyChoices.FRIENDS,
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
