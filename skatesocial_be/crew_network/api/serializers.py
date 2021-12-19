from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers, exceptions
from ..models import FriendRequest, Friendship

User = get_user_model()


class FriendRequestCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ("id", "target")


class FriendRequestRespondSerializer(serializers.Serializer):
    user_response = serializers.IntegerField(required=True)
