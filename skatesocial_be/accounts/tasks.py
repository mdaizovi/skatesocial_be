from django.apps import apps

# TODO: celery
# from skatesocial_be.celery import app


# @app.task()
def update_user_location(user_id, lat, lon):
    User = apps.get_model("accounts.User")
    UserLocation = apps.get_model("accounts.UserLocation")

    user = User.objects.only("location").get(pk=user_id)

    if not hasattr(user, "location"):
        location = UserLocation.objects.create(user=user, lat=lat, lon=lon)
    else:
        location = user.location
        location.lat = lat
        location.lon = lon
        location.save()
