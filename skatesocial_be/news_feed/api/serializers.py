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

    # TODO add view options

    spot = SpotBasicSerializer()

    class Meta:
        model = Event
        fields = (
            "id",
            "created_at",
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

    spot = serializers.PrimaryKeyRelatedField(queryset=Spot.objects.all())
    visible_to_friends = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), many=True
    )
    visible_to_crews = serializers.PrimaryKeyRelatedField(
        queryset=Crew.objects.all(), many=True
    )
    hidden_from_friends = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), many=True
    )
    hidden_from_crews = serializers.PrimaryKeyRelatedField(
        queryset=Crew.objects.all(), many=True
    )

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
