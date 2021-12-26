import json

from django.contrib.auth import get_user_model
from django.test import TestCase

from crew_network.models import Friendship, Crew
from ..models import Event, EventResponse
from skate_spots.models import Spot

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
        self.acquaintance = User.objects.create_user(
            username="acquaintance", email="acquaintance@email.com"
        )
        self.frenemy = User.objects.create_user(
            username="frenemy", email="frenemy@email.com"
        )
        friends = [self.friend, self.other_friend, self.acquaintance, self.collegue]
        for f in friends:
            friendship = Friendship.objects.create()
            friendship.users.set([self.user, f])

        self.bestie_crew = Crew.objects.create(owned_by=self.user)
        self.bestie_crew.members.set([self.best_friend, self.other_friend])
        self.loose_crew = Crew.objects.create(owned_by=self.user)
        self.loose_crew.members.set([self.acquaintance, self.frenemy])

        self.stranger = User.objects.create_user(
            username="stranger", email="strangery@email.com"
        )

        self.spot = Spot.objects.create(name="G3")

    def test_visible_to_user(self):
        pass
        # Hierarchy: most specific wins. ie if person is in hidden_from_crews but in visible_to_friends, they can see.
        # if friend is in both  visible_to_friends and hidden_from_friends, hidden wins.

        # Event with no privacy set should be visible to all friends, invisible to non-friends

        # visible_to_crews should only be visible_to_friends in that crew, same as visible_to_friends. Hidden from everyone else.

        # hidden_from_crews hidden from friends in that crew, same as hidden_from_friends. Visible to everyone else.

        # if visible_to_crews but hidden_from_friend, friend should not see even if is in crew. Hidden to everyone else.

        # hidden_from_crews and visible_to_friend should be visible to that friend, invisible to other crew members. Visible to other friends.

        # if visible_to_crew and hidden_from_crew members intersect, hidden shoud win.

        # if visible_to_friend and hidden_from_friend intersect, hidden shoud win.
