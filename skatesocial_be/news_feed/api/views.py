from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

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
)

User = get_user_model()


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
# Make post reaction
# delete post reaction (undo)
