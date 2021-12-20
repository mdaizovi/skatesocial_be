from itertools import chain
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_exempt

from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import (
    GenericAPIView,
    get_object_or_404,
    CreateAPIView,
    RetrieveUpdateAPIView,
    DestroyAPIView,
    ListAPIView,
)
from rest_framework.permissions import IsAuthenticated
from accounts.api.serializers import UserBasicSerializer
from ..models import FriendRequest, Friendship
from .serializers import FriendRequestCreateSerializer, FriendRequestRespondSerializer

User = get_user_model()


class FriendRequestCreateView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    allowed_methods = ("POST",)

    def get_queryset(self):
        return User.objects.exclude(pk=self.request.user.pk)

    def post(self, request, *args, **kwargs):
        user = request.user
        target = self.get_object()

        # None of those requests should happen, client shouldn't offer possibilty
        # ... just being sure
        # First check to make sure they aren't already friends
        if not Friendship.objects.filter(users=user).filter(users=target).exists():
            # Next check that the friend request doesn't already exist in other direction
            if not FriendRequest.objects.filter(
                initiated_by=target, target=user
            ).exists():
                friend_request, created = FriendRequest.objects.get_or_create(
                    initiated_by=user, target=target
                )
                if created:
                    return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_204_NO_CONTENT)


class FriendRequestRespondView(GenericAPIView):
    serializer_class = FriendRequestRespondSerializer
    permission_classes = (IsAuthenticated,)
    allowed_methods = ("POST",)

    def get_queryset(self):
        return FriendRequest.objects.filter(target=self.request.user)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # no perform create
        user_response = serializer.validated_data["user_response"]
        obj = self.get_object()
        if user_response == 1:
            initiated_by = obj.initiated_by
            target = obj.target
            if (
                not Friendship.objects.filter(users=initiated_by)
                .filter(users=target)
                .exists()
            ):
                with transaction.atomic():
                    friendship = Friendship.objects.create()
                    friendship.users.set([initiated_by, target])
                    obj.delete()
                return Response(status=status.HTTP_201_CREATED)
        elif user_response == 0:
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class FriendRequestCancelView(DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = None
    # allowed_methods = ("DEL",)

    def get_queryset(self):
        return FriendRequest.objects.filter(initiated_by__pk=self.request.user.pk)


class UnfriendView(DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = None
    # allowed_methods = ("DEL",)

    def get_queryset(self):
        return Friendship.objects.filter(users=self.request.user)


class FriendListView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserBasicSerializer

    # def get_queryset(self):
    #     qset_list = [u.users.exclude(pk=user.pk)
    #                  for u in user.friendship_set.all()]
    #     if len(qset_list) > 1:
    #         return qset_list[0].union(**qset_list[1:])
    #     elif len(qset_list) == 1:
    #         qset_list[0]
    #     else:
    #         return Friendship.objects.filter(pk=None)  # empty queryset

    def get_queryset(self):
        qset_list = [
            u.users.exclude(pk=self.request.user.pk)
            for u in self.request.user.friendship_set.all()
        ]
        return list(chain(*qset_list))

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({"users": serializer.data})
