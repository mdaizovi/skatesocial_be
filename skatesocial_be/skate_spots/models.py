from django.contrib.gis.db import models
from django_countries.fields import CountryField

from .model_choices import SpotTypeChoices


class City(models.Model):
    name = models.CharField(max_length=250)
    country = CountryField()


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
