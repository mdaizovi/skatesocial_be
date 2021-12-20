from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

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
            # U to Unfriend
            return {"action": "U", "id": friendship.pk}
        except Friendship.DoesNotExist:
            try:
                friend_request = FriendRequest.objects.get(
                    initiated_by=searching_user, target=obj
                )
                # C for Cancel Friend Request
                return {"action": "C", "id": friend_request.pk}
            except FriendRequest.DoesNotExist:
                try:
                    friend_request = FriendRequest.objects.get(
                        initiated_by=obj, target=searching_user
                    )
                    # R for Respond to Friend Request
                    return {"action": "R", "id": friend_request.pk}
                except FriendRequest.DoesNotExist:
                    pass
        # If no relationship exists, offer to make friends
        return {"action": "F", "id": obj.pk}

    class Meta:
        model = User
        fields = ("id", "username", "name", "email", "connection_options")
