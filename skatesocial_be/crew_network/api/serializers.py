from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers, exceptions
from ..models import FriendRequest, Friendship, Crew
from accounts.api.serializers import UserViewSerializer

User = get_user_model()


class FriendRequestCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ("id",)


class FriendRequestRespondSerializer(serializers.Serializer):
    user_response = serializers.IntegerField(required=True)


class CrewBasicSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False)

    class Meta:
        model = Crew
        fields = ("id", "name")


class CrewUpdateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False)
    members = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)

    class Meta:
        model = Crew
        fields = ("id", "name", "members")


class CrewDetailSerializer(serializers.ModelSerializer):
    name = serializers.CharField(read_only=True)
    members = UserViewSerializer(many=True)

    class Meta:
        model = Crew
        fields = ("id", "name", "members")
