import json

from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Friendship, Crew

User = get_user_model()


class EventCreateEditDeleteTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="Me", email="me@email.com")
        self.best_friend = User.objects.create_user(
            username="best friend", email="best-friend@email.com"
        )
        self.other_friend = User.objects.create_user(
            username="other friend", email="other-friend@email.com"
        )
        friends = [self.best_friend, self.other_friend]
        for f in friends:
            friendship = Friendship.objects.create()
            friendship.users.set([self.user, f])

        self.crew = Crew.objects.create(owned_by=self.user)
        self.crew.members.set([self.best_friend, self.other_friend])

    def test_remove_deleted_friend_from_crews(self):
        self.assertTrue(self.other_friend in [x for x in self.crew.members.all()])
        friendship_query = Friendship.objects.filter(users=self.user).filter(
            users=self.other_friend
        )
        friendship = friendship_query.first()
        friendship.delete()
        self.assertFalse(friendship_query.exists())

        self.assertTrue(self.best_friend in [x for x in self.crew.members.all()])
        self.assertFalse(self.other_friend in [x for x in self.crew.members.all()])
