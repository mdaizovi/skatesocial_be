from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers, exceptions

from skate_spots.api.serializers import SpotBasicSerializer
from skate_spots.models import Spot
from accounts.api.serializers import UserViewSerializer
from crew_network.api.serializers import CrewBasicSerializer
from crew_network.models import Crew

from ..models import Event, EventResponse


User = get_user_model()


class EventViewBasicSerializer(serializers.ModelSerializer):
    """
    Viewing Event if it's not yours
    """

    created_at = serializers.DateTimeField(format="%d-%m-%Y %H:%M")
    start_at = serializers.DateTimeField(format="%d-%m-%Y %H:%M")
    end_at = serializers.DateTimeField(format="%d-%m-%Y %H:%M")
    spot = SpotBasicSerializer()

    class Meta:
        model = Event
        fields = (
            "id",
            "created_at",
            "end_at",
            "start_at",
            "spot",
            "text",
        )


class EventViewDetailSerializer(EventViewBasicSerializer):
    """
    Viewing if it's yours. More detail to visibility, so you can choose who can see it
    """

    visible_to_friends = UserViewSerializer(many=True)
    visible_to_crews = CrewBasicSerializer()
    hidden_from_friends = UserViewSerializer(many=True)
    hidden_from_crews = CrewBasicSerializer()

    class Meta:
        model = Event
        fields = (
            "id",
            "created_at",
            "spot",
            "text",
            "start_at",
            "visible_to_friends",
            "visible_to_crews",
            "hidden_from_friends",
            "hidden_from_crews",
        )


class EventUpdateSerializer(serializers.ModelSerializer):
    """
    For setting Visibility, only has id for setting visibility (not all user/spot info)
    """

    created_at = serializers.DateTimeField(format="%d-%m-%Y %H:%M", required=False)
    start_at = serializers.DateTimeField(format="%d-%m-%Y %H:%M", required=False)
    end_at = serializers.DateTimeField(format="%d-%m-%Y %H:%M", required=False)

    spot = serializers.PrimaryKeyRelatedField(queryset=Spot.objects.all())
    visible_to_friends = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), many=True, required=False
    )
    visible_to_crews = serializers.PrimaryKeyRelatedField(
        queryset=Crew.objects.all(), many=True, required=False
    )
    hidden_from_friends = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), many=True, required=False
    )
    hidden_from_crews = serializers.PrimaryKeyRelatedField(
        queryset=Crew.objects.all(), many=True, required=False
    )

    class Meta:
        model = Event
        fields = (
            "id",
            "created_at",
            "spot",
            "text",
            "start_at",
            "end_at",
            "visible_to_friends",
            "visible_to_crews",
            "hidden_from_friends",
            "hidden_from_crews",
        )


class EventResponseCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventResponse
        fields = (
            "id",
            "rsvp",
        )


class EventResponseViewSerializer(serializers.ModelSerializer):
    event = EventViewBasicSerializer()

    class Meta:
        model = EventResponse
        fields = (
            "id",
            "event",
            "rsvp",
        )
