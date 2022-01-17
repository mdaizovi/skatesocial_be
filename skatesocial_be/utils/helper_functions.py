import math

from timezonefinder import TimezoneFinder
from pytz import timezone as pytz_timezone


def get_timezone_string(lat, lon):
    tf = TimezoneFinder()
    timezone_name = tf.timezone_at(lng=float(lon), lat=float(lat))
    tz = pytz_timezone(timezone_name)
    return str(tz)


def replace_timezone(time_obj, lon, lat):
    tz = get_timezone_string(lon=lon, lat=lat)
    time_obj = time_obj.replace(tzinfo=tz)
    return time_obj


# WHY THE FUCK DO I NEED THIS?!?


def distance_to_decimal_degrees(distance, latitude):
    """
    Source of formulae information:
        1. https://en.wikipedia.org/wiki/Decimal_degrees
        2. http://www.movable-type.co.uk/scripts/latlong.html
    :param distance: an instance of `from django.contrib.gis.measure.Distance`
    :param latitude: y - coordinate of a point/location

    Theatre.objects.filter(geom__dwithin=(GEOSGeometry('POINT(30.111199 -97.309990)'), distance_to_decimal_degrees(D(m=5000), -97.309990)))
    """
    lat_radians = latitude * (math.pi / 180)
    # 1 longitudinal degree at the equator equal 111,319.5m equiv to 111.32km
    return distance.m / (111_319.5 * math.cos(lat_radians))
