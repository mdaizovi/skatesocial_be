from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_exempt

from rest_framework import status
from rest_framework.response import Response

User = get_user_model()
