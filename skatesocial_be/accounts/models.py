from itertools import chain
from django.contrib.gis.db import models

from django.contrib.auth.models import AbstractUser
from django.contrib.gis.geos import fromstr
from django.utils import timezone as django_timezone

from utils.helper_functions import replace_timezone


class User(AbstractUser):
    name = models.CharField(null=True, blank=True, max_length=50)

    class Meta:
        ordering = ("username", "name")

    @property
    def friends(self):
        qset_list = [u.users.exclude(pk=self.pk) for u in self.friendship_set.all()]
        return list(chain(*qset_list))

    @property
    def email_verified(self):
        email = self.emailaddress_set.filter(primary=True).first()
        return email.verified if email else False


class UserLocation(models.Model):
    """
    Created on various requests, used when searching for users in your area.
    Should there only be 1 of these, most reecent?
    Any reason to know where people have been?


    if distance measurements in meters are required (as opposed to simply ordering them
    from nearest to furthest), then the geography PointField will be used.


    """

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="location",
    )
    updated_at = models.DateTimeField(null=True, blank=True)

    lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    lon = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    location = models.PointField(null=True, blank=True, geography=True, srid=4326)

    class Meta:
        ordering = (
            "updated_at",
            "user",
        )

    def _get_location_from_lon_lat(self):
        # Don't save here, save after.
        if not self.location and (self.lon and self.lat):
            self.location = fromstr(
                ("POINT(%s %s)" % (str(self.lon), str(self.lat))), srid=4326
            )

    def save(self, *args, **kwargs):
        # if self.updated_at:
        #     if all([not self.updated_at.tzinfo, self.lon, self.lat]):
        #         self.updated_at = replace_timezone(
        #             time_obj=self.updated_at, lon=self.lon, lat=self.lat)

        # self._get_location_from_lon_lat()

        super().save(*args, **kwargs)
