from django.contrib.gis.db import models
from django.contrib.auth import get_user_model

from django_countries.fields import CountryField
from django.contrib.gis.geos import fromstr, Point

from .model_choices import SpotTypeChoices
from .model_managers import SpotManager

User = get_user_model()

"""
Maps links to look at later
BE
https://hackernoon.com/how-to-build-location-based-app-with-geodjango-bk1i356x
https://pganalyze.com/blog/geodjango-postgis

FE
https://github.com/react-native-maps/react-native-maps
https://www.npmjs.com/package/react-native-maps
https://docs.expo.dev/versions/latest/sdk/map-view/
https://blog.logrocket.com/react-native-maps-introduction/
https://openbase.com/categories/js/best-react-native-map-libraries
https://www.youtube.com/watch?v=mhc8k_PoUJk&ab_channel=ProgrammingwithMash
https://dzone.com/articles/how-to-integrate-google-maps-in-react-native
https://blog.waldo.io/react-native-maps-tutorial-examples/
https://www.youtube.com/watch?v=yEuRPiqppQc&ab_channel=UAStudios
https://stackoverflow.com/questions/51476976/react-native-maps-properties-showspointsofinterest-showsindoors-and-shows


"""


class City(models.Model):
    name = models.CharField(max_length=250)
    country = CountryField()

    def __str__(self):
        return "<{}> {}, {}".format(
            self.__class__.__name__, self.name, self.country.code
        )


class Spot(models.Model):

    name = models.CharField(max_length=250)
    address = models.CharField(max_length=100, null=True, blank=True)
    city = models.ForeignKey(City, null=True, blank=True, on_delete=models.SET_NULL)

    lat = models.DecimalField(max_digits=19, decimal_places=10, null=True, blank=True)
    lon = models.DecimalField(max_digits=19, decimal_places=10, null=True, blank=True)
    location = models.PointField(null=True, blank=True)

    category = models.CharField(
        max_length=1,
        choices=SpotTypeChoices.CHOICES,
        default=SpotTypeChoices.STREET,
    )
    private = models.BooleanField(default=False)
    submitted_by = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL
    )
    objects = SpotManager()

    class Meta:
        ordering = ("name",)

    def __str__(self):
        if self.city and self.city.country:
            return "<{}> {}: {}, {}".format(
                self.__class__.__name__,
                self.name,
                self.city.name,
                self.city.country.code,
            )
        else:
            return "<{}>: {}".format(self.__class__.__name__, self.name)

    def location_from_lon_lat(self):
        # Don't save here, save after.
        if not self.location and (self.lon and self.lat):
            self.location = fromstr(
                ("POINT(%s %s)" % (str(self.lon), str(self.lat))), srid=4326
            )

    def save(self, *args, **kwargs):
        self.location_from_lon_lat()
        super(Spot, self).save()


class SpotAlias(models.Model):

    help_text = "AKA for spots that are commonly called more than 1 thing"
    name = models.CharField(max_length=250)
    spot = models.ForeignKey(Spot, on_delete=models.CASCADE)

    def __str__(self):
        return "<{}>: {} ({})".format(self.__class__.__name__, self.name, self.spot)
