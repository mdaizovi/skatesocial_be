from ..models import Event
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers, exceptions

from skate_spots.models import Spot
from crew_network.models import Crew

User = get_user_model()

# update is PrimaryKeyRelatedField, will need another with a lot more info about spot and visibility


class EventUpdateSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)
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
