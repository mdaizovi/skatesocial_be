from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers, exceptions
from ..models import FriendRequest, Friendship, Crew

User = get_user_model()


class FriendRequestCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ("id",)


class FriendRequestRespondSerializer(serializers.Serializer):
    user_response = serializers.IntegerField(required=True)


class CrewUpdateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False)
    members = serializers.PrimaryKeyRelatedField(
        queryset=Crew.objects.all(), required=False
    )

    class Meta:
        model = Crew
        fields = ("id", "name", "members")
        depth = 1


class CrewMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "name",
            # add image when i add the field
        )


class CrewDetailSerializer(serializers.ModelSerializer):
    name = serializers.CharField(read_only=True)
    members = CrewMemberSerializer()

    class Meta:
        model = Crew
        fields = ("id", "name", "members")
