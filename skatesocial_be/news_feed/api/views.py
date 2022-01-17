import datetime
import pytz

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.gis.geos import fromstr, Point, GEOSGeometry
from django.contrib.gis.measure import D
from django.utils.translation import gettext_lazy as _
from django.db.models import Q

from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import (
    GenericAPIView,
    get_object_or_404,
    CreateAPIView,
    RetrieveUpdateAPIView,
    RetrieveAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated

from utils.helper_functions import get_timezone_string

from ..models import Event, EventResponse
from .serializers import (
    EventUpdateSerializer,
    EventViewBasicSerializer,
    EventViewDetailSerializer,
    EventResponseCreateUpdateSerializer,
)
from accounts.tasks import update_user_location

User = get_user_model()


class NewsFeedHomeAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = None
    allowed_methods = ("GET",)
    """
    Filter needs to include MY posts. I guess otherwise just toss them in.
    """

    def get(self, request, format=None):
        data = {"notifications": [], "events": {"upcoming": [], "past": []}}
        # TODO needs to accept filters in GET
        # Filter needs to include MY posts. Otherwise just toss them in.
        max_events = 25

        # All these should come from client
        lat = self.request.query_params.get("lat", None)
        lon = self.request.query_params.get("lon", None)
        if not (lat and lon):
            return Response(
                {"status": "Required field not found: lat, lon"},
                status=status.HTTP_404_NOT_FOUND,
            )
        # TODO: celery
        update_user_location(user_id=self.request.user.pk, lat=lat, lon=lon)

        now = datetime.datetime.now(
            pytz.timezone(get_timezone_string(lon=lon, lat=lat))
        )
        # max_distance_k is an arbitrary choice I made.
        # Fenny to Stansi is 25 kilometers, Fenny to Potsdam HBF is 35
        max_distance_k = self.request.query_params.get("max_distance_k", 30)
        pnt = GEOSGeometry("POINT({} {})".format(lon, lat), srid=4326)

        base_query = Event.objects.visible_to_user(user=self.request.user).filter(
            spot__location__distance_lte=(pnt, D(km=int(max_distance_k)))
        )

        upcoming_events = base_query.filter(
            Q(start_at__gte=now) | Q(end_at__gte=now)
        ).order_by("start_at")[:max_events]
        past_events = base_query.filter(start_at__lt=now).order_by("-start_at")[
            :max_events
        ]

        data["events"]["upcoming"] = EventViewBasicSerializer(
            upcoming_events, many=True
        ).data
        data["events"]["past"] = EventViewBasicSerializer(past_events, many=True).data

        return Response(data=data, status=status.HTTP_200_OK)


class EventCreateAPIView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = EventUpdateSerializer

    def get_queryset(self):
        return Event.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class EventUpdateAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        if self.request.method == "GET":
            # anything that's visible to you
            return Event.objects.visible_to_user(user=self.request.user)
        else:  # can only patch or delete what you own
            return Event.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        obj = self.get_object()
        if self.request.method == "GET":
            if self.request.user == obj.user:
                return EventViewDetailSerializer
            else:
                return EventViewBasicSerializer
        else:
            return EventUpdateSerializer


# TODO
# TEST the EventResponse endpoints, don't know if they work


class EventResponseCreateAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = EventResponseCreateUpdateSerializer
    allowed_methods = ("POST",)

    def get_queryset(self):
        event_pk = self.kwargs.get("event_pk")
        # Can't respond to an event you can't see.
        visible_events = Event.objects.visible_to_user(user=self.request.user)
        return EventResponse.objects.filter(
            event__pk=event_pk, event__in=visible_events, user=self.request.user
        )

    def post(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        event = get_object_or_404(Event, pk=self.kwargs.get("event_pk"))
        visible_events = Event.objects.visible_to_user(user=self.request.user)

        if event in visible_events:
            if not EventResponse.objects.filter(user=user, event=event).exists():
                rsvp = serializer.validated_data["rsvp"]
                event_response, created = EventResponse.objects.get_or_create(
                    user=user, event=event, rsvp=rsvp
                )
                if created:
                    return Response(status=status.HTTP_201_CREATED)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)


class EventResponseUpdateAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = EventResponseCreateUpdateSerializer
    allowed_methods = ("PATCH", "DEL")

    def get_queryset(self):
        event_pk = self.kwargs.get("event_pk")
        # Can't respond to an event you can't see.
        visible_events = Event.objects.visible_to_user(user=self.request.user)
        return EventResponse.objects.filter(
            event__pk=event_pk, event__in=visible_events, user=self.request.user
        )
