import datetime
from django.utils.translation import gettext_lazy as _

from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework.authentication import BaseAuthentication

decade = datetime.timedelta(days=365 * 10)


class DecadeAccessToken(AccessToken):
    lifetime = decade


class DecadeRefreshToken(RefreshToken):
    lifetime = decade
