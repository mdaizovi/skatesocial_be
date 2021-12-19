from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_exempt

from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import (
    GenericAPIView,
    get_object_or_404,
    CreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated

from ..models import FriendRequest, Friendship
from .serializers import FriendRequestSerializer

User = get_user_model()

# category = get_object_or_404(ContentCategory, id=pk)


class FriendRequestCreateView(CreateAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        user = self.request.user
        target = User.objects.get(pk=self.request.data["target"])

        # First check to make sure they aren't already friends
        if not Friendship.objects.filter(users=user).filter(users=target).exists():
            # Next check that the friend request doesn't already exist in other direction
            if not FriendRequest.objects.filter(
                initiated_by=target, target=user
            ).exists():
                friend_request, created = FriendRequest.objects.get_or_create(
                    initiated_by=user, target=target
                )
        # None of those requests should happen, client shouldn't offer possibilty
        # just being sure


class FriendRequestRespondView(RetrieveUpdateDestroyAPIView):
    # serializer_class = LabelBasicSerializer
    permission_classes = (IsAuthenticated,)
    # allowed_methods = ("GET", "PATCH", "DELETE")

    # def get_queryset(self):
    #     # Show only default labels and user-owned labels
    #     return FriendRequest.objects.get_default_or_owned(self.request.user)
    def perform_create(self, serializer):
        pass
        # create Friendship
