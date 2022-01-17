from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

from rest_framework import serializers, exceptions

from auth.api.serializers import UserBasicSerializer
from crew_network.models import Friendship, FriendRequest

User = get_user_model()


class UserSearchResultsSerializer(UserBasicSerializer):
    connection_options = serializers.SerializerMethodField()

    def get_connection_options(self, obj):
        request = self.context["request"]
        searching_user = request.user
        try:
            friendship = Friendship.objects.filter(users=obj).get(users=searching_user)
            # Unfriend
            next_request = {
                "url": reverse("remove-friend", args=(friendship.pk,)),
                "method": "DEL",
                "payload": {},
            }
            return [{"text": "Unfriend", "icon": "TBD", "next": next_request}]

        except Friendship.DoesNotExist:
            try:
                friend_request = FriendRequest.objects.get(
                    initiated_by=searching_user, target=obj
                )
                # C for Cancel Friend Request
                next_request = {
                    "url": reverse("friend-request-action", args=(friend_request.pk,)),
                    "method": "DEL",
                    "payload": {},
                }
                return [
                    {
                        "text": "Cancel friend request",
                        "icon": "TBD",
                        "next": next_request,
                    }
                ]
            except FriendRequest.DoesNotExist:
                try:
                    friend_request = FriendRequest.objects.get(
                        initiated_by=obj, target=searching_user
                    )
                    # R for Respond to Friend Request
                    approve = {
                        "url": reverse(
                            "friend-request-action", args=(friend_request.pk,)
                        ),
                        "method": "PATCH",
                        "payload": {"user_response": 1},
                    }
                    reject = {
                        "url": reverse(
                            "friend-request-action", args=(friend_request.pk,)
                        ),
                        "method": "PATCH",
                        "payload": {"user_response": 0},
                    }
                    return [
                        {
                            "text": "Approve friend request",
                            "icon": "TBD",
                            "next": approve,
                        },
                        {
                            "text": "Reject friend request",
                            "icon": "TBD",
                            "next": reject,
                        },
                    ]
                except FriendRequest.DoesNotExist:
                    pass
        # If no relationship exists, offer to make friends
        next_request = [
            {
                "url": reverse("add-friend"),
                "method": "POST",
                "payload": {"target": obj.pk},
            }
        ]
        return [{"text": "Send friend request", "icon": "TBD", "next": next_request}]

    class Meta:
        model = User
        fields = ("id", "username", "name", "email", "connection_options")
