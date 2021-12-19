import json

from django.contrib.auth import get_user_model
from django.test import TestCase

from django.test.client import encode_multipart

from rest_framework.test import APIRequestFactory, APITestCase

from ..models import FriendRequest, Friendship

User = get_user_model()

# print(response.status_code)
# print(response.data)


class FriendRequestTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="Me", email="me@email.com")
        self.target = User.objects.create_user(
            username="friend", email="friend@email.com"
        )
        self.client.force_authenticate(user=self.user)

        self.friend_request_query_by_me = FriendRequest.objects.filter(
            initiated_by=self.user, target=self.target
        )
        self.friend_request_query_by_target = FriendRequest.objects.filter(
            initiated_by=self.target, target=self.user
        )
        self.friendship_exists_query = Friendship.objects.filter(
            users=self.user
        ).filter(users=self.target)

    def test_friend_request_create_view(self):

        # Assert can make friend request
        # Assert users aren't already friends
        self.assertEqual(self.friendship_exists_query.count(), 0)
        response = self.client.post(
            "/api/network/add-friend/{}/".format(self.target.pk)
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(self.friendship_exists_query.count(), 0)

        self.assertEqual(self.friend_request_query_by_me.count(), 1)
        self.assertEqual(self.friend_request_query_by_target.count(), 0)

        # Assert double post won't make a duplicate record
        response = self.client.post(
            "/api/network/add-friend/{}/".format(self.target.pk)
        )
        self.assertEqual(response.status_code, 204)
        self.assertEqual(self.friendship_exists_query.count(), 0)
        self.assertEqual(self.friend_request_query_by_me.count(), 1)

        # Assert if we're already friends nothing happens
        FriendRequest.objects.get(initiated_by=self.user, target=self.target).delete()
        friendship = Friendship.objects.create()
        friendship.users.set([self.user, self.target])
        response = self.client.post(
            "/api/network/add-friend/{}/".format(self.target.pk)
        )
        self.assertEqual(response.status_code, 204)
        self.assertEqual(self.friendship_exists_query.count(), 1)
        self.assertEqual(self.friend_request_query_by_me.count(), 0)
        self.assertEqual(self.friend_request_query_by_target.count(), 0)

    def test_friend_request_respond_view(self):
        friend_request = FriendRequest.objects.create(
            initiated_by=self.target, target=self.user
        )
        self.assertEqual(self.friend_request_query_by_target.count(), 1)

        # Wrong number in request does nothing
        response = self.client.post(
            "/api/network/friend-request-respond/{}/".format(friend_request.pk),
            {"user_response": 3},
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.friendship_exists_query.count(), 0)
        self.assertEqual(self.friend_request_query_by_me.count(), 0)
        self.assertEqual(self.friend_request_query_by_target.count(), 1)

        # 0 deletes the friend request
        response = self.client.post(
            "/api/network/friend-request-respond/{}/".format(friend_request.pk),
            {"user_response": 0},
        )
        self.assertEqual(response.status_code, 204)
        self.assertEqual(self.friendship_exists_query.count(), 0)
        self.assertEqual(self.friend_request_query_by_me.count(), 0)
        self.assertEqual(self.friend_request_query_by_target.count(), 0)

        # 1 accepts the friend request, makes Friendship
        # but first lets remake the friend request
        friend_request = FriendRequest.objects.create(
            initiated_by=self.target, target=self.user
        )
        response = self.client.post(
            "/api/network/friend-request-respond/{}/".format(friend_request.pk),
            {"user_response": 1},
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(self.friendship_exists_query.count(), 1)
        self.assertEqual(self.friend_request_query_by_me.count(), 0)
        self.assertEqual(self.friend_request_query_by_target.count(), 0)

    def test_friend_request_cancel_view(self):
        friend_request = FriendRequest.objects.create(
            initiated_by=self.user, target=self.target
        )
        self.assertEqual(self.friend_request_query_by_me.count(), 1)
        response = self.client.delete(
            "/api/network/friend-request-cancel/{}/".format(friend_request.pk)
        )
        self.assertEqual(response.status_code, 204)
        self.assertEqual(self.friend_request_query_by_me.count(), 0)

    def test_unfriend_view(self):
        friendship = Friendship.objects.create()
        friendship.users.set([self.user, self.target])
        self.assertEqual(self.friendship_exists_query.count(), 1)
        response = self.client.delete(
            "/api/network/remove-friend/{}/".format(friendship.pk)
        )
        self.assertEqual(response.status_code, 204)
        self.assertEqual(self.friendship_exists_query.count(), 0)
        # assert friend didn't get deleted!
        self.assertEqual(User.objects.filter(pk=self.target.pk).count(), 1)
