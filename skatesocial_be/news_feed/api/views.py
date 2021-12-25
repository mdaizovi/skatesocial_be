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
    DestroyAPIView,
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated

from ..models import Event, EventResponse
from .serializers import EventUpdateSerializer

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
    serializer_class = EventUpdateSerializer
    allowed_methods = ("PATCH", "DELETE")

    def get_queryset(self):
        return Event.objects.filter(user=self.request.user)

    # def get_serializer_class(self):
    #     pass
    # if self.action == 'list':
    #     return serializers.ListaGruppi
    # if self.action == 'retrieve':
    #     return serializers.DettaglioGruppi
    # return serializers.Default # I dont' know what you want for create/destroy/update.


# Event View, for looking at other people's posts. obv with limited permissions.
# Make post reaction
# delete post reaction (undo)
