import json

from django.contrib.auth import get_user_model
from django.test import TestCase

from django.test.client import encode_multipart

from rest_framework.test import APIRequestFactory, APITestCase

from crew_network.models import FriendRequest, Friendship

User = get_user_model()


class SearchResultsSerializerTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="Me", email="me@email.com")
        self.target = User.objects.create_user(
            username="friend", name="My Friend", email="friend@email.com"
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

    def test_user_search_results_serializer(self):

        # First we're not friends, so offer to make it so.
        self.assertEqual(self.friendship_exists_query.count(), 0)
        response = self.client.get("/api/search/", {"search": self.target.email})
        self.assertEqual(response.status_code, 200)
        search_results_users = response.data["users"]
        connection_options = search_results_users[0]["connection_options"]
        # self.assertEqual(connection_options["action"], "F")
        self.assertEqual(connection_options, {"action": "F"})

        # Make us friends, offer to unfriend and provide friendship id
        friendship = Friendship.objects.create()
        friendship.users.set([self.user, self.target])
        response = self.client.get("/api/search/", {"search": self.target.email})
        self.assertEqual(response.status_code, 200)
        search_results_users = response.data["users"]
        connection_options = search_results_users[0]["connection_options"]
        self.assertEqual(connection_options, {"action": "U", "id": friendship.pk})
        friendship.delete()

        # Make a friend request from me, offer to cancel the friend request and offer friend request id
        friend_request = FriendRequest.objects.create(
            initiated_by=self.user, target=self.target
        )
        response = self.client.get("/api/search/", {"search": self.target.email})
        self.assertEqual(response.status_code, 200)
        search_results_users = response.data["users"]
        connection_options = search_results_users[0]["connection_options"]
        self.assertEqual(connection_options, {"action": "C", "id": friend_request.pk})
        friend_request.delete()

        # Make a friend request to me, offer to respond to the friend request and offer friend request id
        friend_request = FriendRequest.objects.create(
            initiated_by=self.target, target=self.user
        )
        response = self.client.get("/api/search/", {"search": self.target.email})
        self.assertEqual(response.status_code, 200)
        search_results_users = response.data["users"]
        connection_options = search_results_users[0]["connection_options"]
        self.assertEqual(connection_options, {"action": "R", "id": friend_request.pk})
        friend_request.delete()
