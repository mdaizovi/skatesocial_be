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
        self.no_crew_friend = User.objects.create_user(
            username="no_crew", email="no_crew@email.com"
        )
        friends = [
            self.best_friend,
            self.other_friend,
            self.acquaintance,
            self.frenemy,
            self.no_crew_friend,
        ]
        for f in friends:
            friendship = Friendship.objects.create()
            friendship.users.set([self.user, f])

        self.bestie_crew = Crew.objects.create(owned_by=self.user, name="bestie_crew")
        self.bestie_crew.members.set([self.best_friend, self.other_friend])
        self.loose_crew = Crew.objects.create(owned_by=self.user, name="loose_crew")
        self.loose_crew.members.set([self.acquaintance, self.frenemy])

        self.stranger = User.objects.create_user(
            username="stranger", email="strangery@email.com"
        )

        self.spot = Spot.objects.create(name="G3")

    def test_visible_to_user(self):
        # Hierarchy: most specific wins. ie if person is in hidden_from_crews but in visible_to_friends, they can see.
        # if friend is in both visible_to_friends and hidden_from_friends, hidden wins.
        # ---
        event = Event.objects.create(user=self.user, spot=self.spot)
        # Event with no privacy set should be visible to all friends regardless of crew, invisible to non-friends
        self.assertTrue(event in [e for e in Event.objects.visible_to_user(self.user)])
        self.assertTrue(
            event in [e for e in Event.objects.visible_to_user(self.best_friend)]
        )
        self.assertTrue(
            event in [e for e in Event.objects.visible_to_user(self.no_crew_friend)]
        )
        self.assertFalse(
            event in [e for e in Event.objects.visible_to_user(self.stranger)]
        )

        # visible_to_crews should only be visible_to_friends in that crew, same as visible_to_friends. Hidden from everyone else.
        event.visible_to_crews.add(self.bestie_crew)
        self.assertTrue(event in [e for e in Event.objects.visible_to_user(self.user)])
        self.assertTrue(
            event in [e for e in Event.objects.visible_to_user(self.best_friend)]
        )
        self.assertFalse(
            event in [e for e in Event.objects.visible_to_user(self.frenemy)]
        )
        self.assertFalse(
            event in [e for e in Event.objects.visible_to_user(self.no_crew_friend)]
        )
        self.assertFalse(
            event in [e for e in Event.objects.visible_to_user(self.stranger)]
        )
        # (reset this block)
        event.visible_to_crews.clear()

        # hidden_from_crews hidden from friends in that crew, same as hidden_from_friends. Visible to everyone else.
        event.hidden_from_crews.add(self.loose_crew)
        self.assertTrue(event in [e for e in Event.objects.visible_to_user(self.user)])
        self.assertTrue(
            event in [e for e in Event.objects.visible_to_user(self.best_friend)]
        )
        self.assertTrue(
            event in [e for e in Event.objects.visible_to_user(self.no_crew_friend)]
        )
        self.assertFalse(
            event in [e for e in Event.objects.visible_to_user(self.frenemy)]
        )
        self.assertFalse(
            event in [e for e in Event.objects.visible_to_user(self.stranger)]
        )
        # (reset this block)
        event.hidden_from_crews.clear()

        # if visible_to_crews but hidden_from_friend, friend should not see even if is in crew. Hidden to everyone else.
        event.visible_to_crews.add(self.bestie_crew)
        self.assertTrue(event in [e for e in Event.objects.visible_to_user(self.user)])
        event.hidden_from_friends.add(self.other_friend)
        self.assertTrue(
            event in [e for e in Event.objects.visible_to_user(self.best_friend)]
        )
        self.assertFalse(
            event in [e for e in Event.objects.visible_to_user(self.other_friend)]
        )
        self.assertFalse(
            event in [e for e in Event.objects.visible_to_user(self.no_crew_friend)]
        )
        self.assertFalse(
            event in [e for e in Event.objects.visible_to_user(self.frenemy)]
        )
        self.assertFalse(
            event in [e for e in Event.objects.visible_to_user(self.stranger)]
        )
        # (reset this block)
        event.visible_to_crews.clear()
        event.hidden_from_friends.clear()

        # NOTE hidden_from_crews and visible_to_friend are incompatible together and shouldn't be offered.
