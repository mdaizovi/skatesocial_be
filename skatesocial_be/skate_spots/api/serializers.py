from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers, exceptions

from ..models import Spot

# User = get_user_model()


class SpotBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Spot
        fields = ("id", "name", "category", "private")
