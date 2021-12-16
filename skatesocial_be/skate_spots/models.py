from django.contrib.gis.db import models
from django.contrib.auth import get_user_model

from django_countries.fields import CountryField

from .model_choices import SpotTypeChoices

User = get_user_model()


class City(models.Model):
    name = models.CharField(max_length=250)
    country = CountryField()

    def __str__(self):
        return "<{}> {}, {}".format(
            self.__class__.__name__, self.name, self.country.code
        )


class Spot(models.Model):

    name = models.CharField(max_length=250)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100, null=True, blank=True)

    lat = models.DecimalField(max_digits=19, decimal_places=10, null=True, blank=True)
    lon = models.DecimalField(max_digits=19, decimal_places=10, null=True, blank=True)
    location = models.PointField(null=True, blank=True)

    category = models.CharField(
        max_length=1,
        choices=SpotTypeChoices.CHOICES,
        default=SpotTypeChoices.STREET,
    )
    submitted_by = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL
    )

    def __str__(self):
        return "<{}> {}: {}, {}".format(
            self.__class__.__name__, self.name, self.city.name, self.city.country.code
        )
