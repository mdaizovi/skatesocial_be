from datetime import timedelta
import json
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.test.client import encode_multipart
from django.utils import timezone as django_timezone

from rest_framework.test import APIRequestFactory, APITestCase
from crew_network.models import Friendship
from ..models import Event, EventResponse
from ..model_choices import EventResponseChoices
from skate_spots.models import Spot

from utils.helper_functions import replace_timezone, get_timezone_string

User = get_user_model()

# print(response.status_code)
# print(response.data)


class NewsFeedHomeAPIViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="Me", email="me@email.com")
        self.nearby_friend = User.objects.create_user(username="neaby friend")
        self.friend = User.objects.create_user(username="friend")
        for f in [self.friend]:
            friendship = Friendship.objects.create()
            friendship.users.set([self.user, f])

        self.lat = Decimal(52.5239766)
        self.lon = Decimal(13.4794608)
        self.close_spot = Spot.objects.create(
            name="G3", lat=Decimal(52.4969355), lon=Decimal(13.3695167)
        )
        self.faraway_spot = Spot.objects.create(
            name="Bowl Bar", lat=Decimal(50.070533), lon=Decimal(14.4513379)
        )
        self.url = "/api/v1/news/feed/home"
        self.client.force_authenticate(user=self.user)

    def test_past_and_upcoming_distinguished(self):
        now = django_timezone.now()
        tomorrow = now + timedelta(days=1)
        yesterday = now - timedelta(days=1)

        attrs = {"user": self.friend, "spot": self.close_spot}
        future_event = Event.objects.create(
            **attrs, start_at=tomorrow, end_at=tomorrow + timedelta(hours=2)
        )
        past_event = Event.objects.create(
            **attrs, start_at=yesterday, end_at=yesterday + timedelta(hours=2)
        )

        response = self.client.get(
            "{}?lat={}&lon={}".format(self.url, self.lat, self.lon), format="json"
        )

        print("\n\n")
        print(json.dumps(response.json(), indent=4, sort_keys=True))

        self.assertEqual(response.status_code, 200)
        future_event_ids = [x["id"] for x in response.data["events"]["upcoming"]]
        self.assertTrue(future_event.pk in future_event_ids)
        self.assertFalse(past_event.pk in future_event_ids)

        past_event_ids = [x["id"] for x in response.data["events"]["past"]]
        self.assertFalse(future_event.pk in past_event_ids)
        self.assertTrue(past_event.pk in past_event_ids)

    def test_distance_affects_visibiity(self):
        now = django_timezone.now()
        tomorrow = now + timedelta(days=1)

        attrs = {
            "user": self.friend,
            "start_at": tomorrow,
            "end_at": tomorrow + timedelta(hours=2),
        }
        close_event = Event.objects.create(**attrs, spot=self.close_spot)
        far_event = Event.objects.create(**attrs, spot=self.faraway_spot)

        response = self.client.get(
            "{}?lat={}&lon={}".format(self.url, self.lat, self.lon)
        )
        self.assertEqual(response.status_code, 200)
        event_ids = [x["id"] for x in response.data["events"]["upcoming"]]
        self.assertTrue(close_event.pk in event_ids)
        self.assertFalse(far_event.pk in event_ids)


class EventCreateEditDeleteTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="Me", email="me@email.com")
        self.friend = User.objects.create_user(
            username="friend", email="friend@email.com"
        )
        friendship = Friendship.objects.create()
        friendship.users.set([self.user, self.friend])
        self.frenemy = User.objects.create_user(
            username="frenemy", email="frenemy@email.com"
        )
        self.spot = Spot.objects.create(name="G3")
        self.event_text = "Come Skate with me :-)"
        self.client.force_authenticate(user=self.user)

        self.event_url = "/api/v1/news/events"

    def test_event_create_view(self):
        # Assert no events right now
        self.assertEqual(self.user.event_set.count(), 0)

        # Assert can make event
        response = self.client.post(
            self.event_url, {"spot": self.spot.pk}, format="json"
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(self.user.event_set.count(), 1)

        # Assert event is as we intended
        event = self.user.event_set.first()
        self.assertEqual(event.spot.pk, self.spot.pk)

        # Clean up
        event.delete()

    def test_event_edit_view(self):
        # Make event
        event = Event.objects.create(
            user=self.user, spot=self.spot, text=self.event_text
        )

        # Assert can update event
        text2 = "Nevermind, rain :-("
        response = self.client.patch(
            self.event_url + "/{}".format(event.pk), {"text": text2}
        )
        self.assertEqual(response.status_code, 200)
        event.refresh_from_db()
        # Spot hasn't changed...
        self.assertEqual(event.spot, self.spot)
        # ... but the text has
        self.assertEqual(event.text, text2)

        # Assert friend can't change your event
        self.client.force_authenticate(user=self.friend)
        response = self.client.patch(
            self.event_url + "/{}".format(event.pk), {"text": self.event_text}
        )
        self.assertEqual(response.status_code, 404)
        event.refresh_from_db()
        # Assert it hasn't changed, it's still text2 from self.user's last update
        self.assertEqual(event.text, text2)

        # Clean up
        self.client.force_authenticate(user=self.user)
        event.delete()

    def test_event_serializer_detail(self):
        # Create event
        event = Event.objects.create(
            user=self.user, spot=self.spot, text=self.event_text
        )
        # I should see visibility details if it's my Event
        response = self.client.get(self.event_url + "/{}".format(event.pk))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("visible_to_friends" in response.data)
        self.assertTrue("visible_to_crews" in response.data)
        self.assertTrue("hidden_from_friends" in response.data)
        self.assertTrue("hidden_from_crews" in response.data)

        # Log in as friend, should not see visibility details
        self.client.force_authenticate(user=self.friend)
        response = self.client.get(self.event_url + "/{}".format(event.pk))
        self.assertEqual(response.status_code, 200)
        self.assertFalse("visible_to_friends" in response.data)
        self.assertFalse("visible_to_crews" in response.data)
        self.assertFalse("hidden_from_friends" in response.data)
        self.assertFalse("hidden_from_crews" in response.data)

        # Frenemy should not see it at all
        self.client.force_authenticate(user=self.frenemy)
        response = self.client.get(self.event_url + "/{}".format(event.pk))
        self.assertEqual(response.status_code, 404)

        # Clean up
        self.client.force_authenticate(user=self.user)
        event.delete()

    def test_event_visibility(self):
        # TODO
        pass

    def test_event_delete(self):
        # Create event
        event = Event.objects.create(
            user=self.user, spot=self.spot, text=self.event_text
        )
        event_pk = event.pk

        # Log in as friend, try to delete. Should fail
        self.client.force_authenticate(user=self.friend)
        response = self.client.delete(self.event_url + "/{}".format(event.pk))
        self.assertEqual(response.status_code, 404)
        self.assertTrue(Event.objects.filter(pk=event_pk).exists())

        # Log in as user, try to delete. Should work.
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.event_url + "/{}".format(event.pk))
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Event.objects.filter(pk=event_pk).exists())


class EventResponseCreateEditDeleteTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="Me", email="me@email.com")
        self.friend = User.objects.create_user(
            username="friend", email="friend@email.com"
        )
        friendship = Friendship.objects.create()
        friendship.users.set([self.user, self.friend])
        self.stranger = User.objects.create_user(
            username="stranger", email="stranger@email.com"
        )
        self.spot = Spot.objects.create(name="G3")
        self.event = Event.objects.create(user=self.friend, spot=self.spot)
        self.client.force_authenticate(user=self.user)

    def test_event_response_create_view(self):
        # Assert no eventsresponse right now
        self.assertEqual(self.user.eventresponse_set.count(), 0)

        url = self.event.get_create_response_url()

        # Assert nothing will happen if option is not in EventResponseChoices
        response = self.client.post(url, {"rsvp": "X"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.user.eventresponse_set.count(), 0)

        # Assert can make eventresponse if code is accepted
        response = self.client.post(url, {"rsvp": EventResponseChoices.GOING})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(self.user.eventresponse_set.count(), 1)

        # Assert multiple eventresponse will not be created
        response = self.client.post(url, {"rsvp": EventResponseChoices.GOING})
        self.assertEqual(response.status_code, 204)
        self.assertEqual(self.user.eventresponse_set.count(), 1)

        # Assert stranger cannot make event response
        self.client.force_authenticate(user=self.stranger)
        response = self.client.post(url, {"rsvp": EventResponseChoices.GOING})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(self.stranger.eventresponse_set.count(), 0)

        # Clean up
        self.client.force_authenticate(user=self.user)
        eventresponse = self.user.eventresponse_set.first()
        eventresponse.delete()

    def test_event_response_update_view(self):
        eventresponse = EventResponse.objects.create(
            user=self.user, event=self.event, rsvp=EventResponseChoices.MAYBE
        )
        self.assertEqual(eventresponse.rsvp, EventResponseChoices.MAYBE)
        url = eventresponse.get_update_url()

        # Assert can update my own event response
        response = self.client.patch(url, {"rsvp": EventResponseChoices.GOING})
        self.assertEqual(response.status_code, 200)
        eventresponse.refresh_from_db()
        self.assertEqual(eventresponse.rsvp, EventResponseChoices.GOING)

        # Assert sending a bad rsvp doesn't save bad value
        response = self.client.patch(url, {"rsvp": "X"})
        self.assertEqual(response.status_code, 400)
        eventresponse.refresh_from_db()
        self.assertEqual(eventresponse.rsvp, EventResponseChoices.GOING)

        # Assert friend can't update my event response
        self.client.force_authenticate(user=self.stranger)
        response = self.client.patch(url, {"rsvp": EventResponseChoices.NOT_GOING})
        self.assertEqual(response.status_code, 404)
        eventresponse.refresh_from_db()
        self.assertEqual(eventresponse.rsvp, EventResponseChoices.GOING)

        # Clean up
        self.client.force_authenticate(user=self.user)
        eventresponse.delete()

    def test_event_response_delete_view(self):
        eventresponse = EventResponse.objects.create(
            user=self.user, event=self.event, rsvp=EventResponseChoices.MAYBE
        )
        eventresponse_pk = eventresponse.pk
        url = eventresponse.get_update_url()

        # Assert stranger can't delete my own event response
        self.client.force_authenticate(user=self.stranger)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 404)
        self.assertTrue(EventResponse.objects.filter(pk=eventresponse_pk).exists())

        # Assert I can delete my own
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(EventResponse.objects.filter(pk=eventresponse_pk).exists())
