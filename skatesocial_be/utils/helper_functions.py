from timezonefinder import TimezoneFinder
from pytz import timezone as pytz_timezone


def get_timezone_string(lat, lon):
    tf = TimezoneFinder()
    timezone_name = tf.timezone_at(lng=lon, lat=lat)
    tz = pytz_timezone(timezone_name)
    return tz
