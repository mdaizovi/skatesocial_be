from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
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

from ..models import Event, EventResponse
from .serializers import (
    EventUpdateSerializer,
    EventViewBasicSerializer,
    EventViewDetailSerializer,
    EventResponseCreateUpdateSerializer,
)

User = get_user_model()


class NewsFeedHomeAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = None
    allowed_methods = ("GET",)
    """
    Filter needs to include MY posts. i guess otherwise just toss them in.
    """

    def get(self, request, format=None):
        data = {"notifications": [], "events": {"upcoming": [], "past": []}}
        # TODO needs to accept filters in GET
        # Filter needs to include MY posts. Otherwise just toss them in.
        now = ""  # need to get user time zone for now.
        max_events = 25

        upcoming_events = (
            Event.objects.visible_to_user(user=self.request.user)
            .filter(Q(start_at__gte=now) | Q(end_at__gte=now))
            .order_by("start_at")[:max_events]
        )
        past_events = (
            Event.objects.visible_to_user(user=self.request.user)
            .filter(start_at__lt=now)
            .order_by("-start_at")[:max_events]
        )

        data["events"]["upcoming"] = EventViewBasicSerializer(upcoming_events).data
        data["events"]["past"] = EventViewBasicSerializer(past_events).data

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
