import json

from django.contrib.auth import get_user_model
from django.test import TestCase

from django.test.client import encode_multipart

from rest_framework.test import APIRequestFactory, APITestCase

from ..models import Event, EventResponse
from skate_spots.models import Spot

User = get_user_model()

# print(response.status_code)
# print(response.data)


class EventCreateEditDeleteTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="Me", email="me@email.com")
        self.friend = User.objects.create_user(
            username="friend", email="friend@email.com"
        )
        self.other_friend = User.objects.create_user(
            username="frenemy", email="frenemy@email.com"
        )
        self.spot = Spot.objects.create(name="G3")
        self.event_text = "Come Skate with me :-)"
        self.client.force_authenticate(user=self.user)

        self.create_url = "/api/news/event/create/"
        self.edit_url = "/api/news/event/edit/"
        self.view_url = "/api/news/event/"

    def test_event_create_view(self):
        # Assert no events right now
        self.assertEqual(self.user.event_set.count(), 0)

        # Assert can make event
        response = self.client.post(self.create_url, {"spot": self.spot.pk})
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
            self.edit_url + "{}/".format(event.pk), {"text": text2}
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
            self.edit_url + "{}/".format(event.pk), {"text": self.event_text}
        )
        self.assertEqual(response.status_code, 404)
        event.refresh_from_db()
        # Assert it hasn't changed, it's still text2 from self.user's last update
        self.assertEqual(event.text, text2)

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
        response = self.client.delete(self.edit_url + "{}/".format(event.pk))
        self.assertEqual(response.status_code, 404)
        self.assertTrue(Event.objects.filter(pk=event_pk).exists())

        # Log in as user, try to delete. Should work.
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.edit_url + "{}/".format(event.pk))
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Event.objects.filter(pk=event_pk).exists())
