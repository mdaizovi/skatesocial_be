import json

from django.contrib.auth import get_user_model
from django.test import TestCase

from django.test.client import encode_multipart

from rest_framework.test import APIRequestFactory, APITestCase

from ..models import FriendRequest, Friendship, Crew

User = get_user_model()

# print(response.status_code)
# print(response.data)


class CrewCreateEditDeleteTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="Me", email="me@email.com")
        self.friend = User.objects.create_user(
            username="friend", email="friend@email.com"
        )
        self.other_friend = User.objects.create_user(
            username="other_friend", email="other_friend@email.com"
        )
        self.client.force_authenticate(user=self.user)
        self.crew_name = "Best Crew"
        self.create_url = "/api/network/crew/create/"
        self.edit_url = "/api/network/crew/edit/"

    def test_crew_create_view(self):
        # Assert no crews right now
        self.assertEqual(self.user.crews_owned.count(), 0)

        # Assert can make crew
        response = self.client.post(
            self.create_url,
            {"name": self.self.crew_name, "members": [self.friend.pk]},
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(self.user.crews_owned.count(), 1)

        # Assert friend is in crew
        crew = self.user.crews_owned.first()
        self.assertEqual(crew.members.count(), 1)
        self.assertTrue(self.friend in crew.members.all())

        # Assert crew owner is user
        self.assertEqual(crew.owner, self.user)

        # Clean up
        crew.delete()

    def test_crew_edit_view(self):
        # Assert no crews right now
        self.assertEqual(self.user.crews_owned.count(), 0)

        crew = Crew.objects.create(owned_by=self.user, name=self.crew_name)
        # Update Crew
        other_name = "Something Different"
        self.client.patch(
            self.edit_url + "{}/".format(crew.pk),
            {"name": other_name, "members": [self.friend.pk, self.other_friend.pk]},
        )
        crew.refresh_from_db()
        self.assertTrue(self.friend in crew.members.all())
        self.assertTrue(self.other_friend in crew.members.all())

        # Assert removing user from list of users removes them from crew
        self.client.patch(
            self.edit_url + "{}/".format(crew.pk),
            {"name": other_name, "members": [self.friend.pk]},
        )
        crew.refresh_from_db()
        self.assertTrue(self.friend in crew.members.all())
        self.assertFalse(self.other_friend in crew.members.all())

        # Clean up
        crew.delete()

    def test_crew_delete_view(self):
        # Assert no crews right now
        self.assertEqual(self.user.crews_owned.count(), 0)

        # Set up a crew
        crew = Crew.objects.create(owned_by=self.user, name=self.crew_name)
        crew.save()
        crew.members.add(self.friend)
        self.assertEqual(self.user.crews_owned.count(), 1)

        # Delete crew
        response = self.client.delete(self.edit_url + "{}/".format(crew.pk))
        self.assertEqual(response.status_code, 204)
        self.assertEqual(self.user.crews_owned.count(), 0)

        # Can't delete a crew that's not owned by me
        crew = Crew.objects.create(owned_by=self.friend, name=self.crew_name)
        crew.save()
        crew_pk = crew.pk
        crew.members.add(self.user)
        self.assertEqual(response.status_code, 204)
        self.assertTrue(Crew.objects.filter(pk=crew_pk).exists())

        # Clean up
        crew.delete()


class FriendRequestTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="Me", email="me@email.com")
        self.target = User.objects.create_user(
            username="friend", email="friend@email.com"
        )

        self.add_friend_url = "/api/network/friends/add/"
        self.respond_friend_url = "/api/network/friend-request/respond/"
        self.cancel_friend_url = "/api/network/friend-request/cancel/"
        self.unfriend_url = "/api/network/friends/remove/"

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
        response = self.client.post(self.add_friend_url + "{}/".format(self.target.pk))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(self.friendship_exists_query.count(), 0)

        self.assertEqual(self.friend_request_query_by_me.count(), 1)
        self.assertEqual(self.friend_request_query_by_target.count(), 0)

        # Assert double post won't make a duplicate record
        response = self.client.post(self.add_friend_url + "{}/".format(self.target.pk))
        self.assertEqual(response.status_code, 204)
        self.assertEqual(self.friendship_exists_query.count(), 0)
        self.assertEqual(self.friend_request_query_by_me.count(), 1)

        # Assert if we're already friends nothing happens
        FriendRequest.objects.get(initiated_by=self.user, target=self.target).delete()
        friendship = Friendship.objects.create()
        friendship.users.set([self.user, self.target])
        response = self.client.post(self.add_friend_url + "{}/".format(self.target.pk))
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
            self.respond_friend_url + "{}/".format(friend_request.pk),
            {"user_response": 3},
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.friendship_exists_query.count(), 0)
        self.assertEqual(self.friend_request_query_by_me.count(), 0)
        self.assertEqual(self.friend_request_query_by_target.count(), 1)

        # 0 deletes the friend request
        response = self.client.post(
            self.respond_friend_url + "{}/".format(friend_request.pk),
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
            self.respond_friend_url + "{}/".format(friend_request.pk),
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
            self.cancel_friend_url + "{}/".format(friend_request.pk)
        )
        self.assertEqual(response.status_code, 204)
        self.assertEqual(self.friend_request_query_by_me.count(), 0)

    def test_unfriend_view(self):
        friendship = Friendship.objects.create()
        friendship.users.set([self.user, self.target])
        self.assertEqual(self.friendship_exists_query.count(), 1)
        response = self.client.delete(self.unfriend_url + "{}/".format(friendship.pk))
        self.assertEqual(response.status_code, 204)
        self.assertEqual(self.friendship_exists_query.count(), 0)
        # assert friend didn't get deleted!
        self.assertEqual(User.objects.filter(pk=self.target.pk).count(), 1)
