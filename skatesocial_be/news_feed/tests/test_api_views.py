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

        # Assert can update event
        event = self.user.event_set.first()
        text = "Come Skate with me!"
        response = self.client.patch(
            self.edit_url + "{}/".format(event.pk), {"text": text}
        )
        self.assertEqual(response.status_code, 200)
        event.refresh_from_db()
        self.assertEqual(event.text, text)

        # Assert can delete event
        response = self.client.delete(
            self.edit_url + "{}/".format(event.pk), {"text": text}
        )
        self.assertEqual(response.status_code, 204)
        self.assertEqual(self.user.event_set.count(), 0)

    def test_event_visibility(self):
        pass

    # def test_crew_edit_view(self):
    #     # Assert no crews right now
    #     self.assertEqual(self.user.crews_owned.count(), 0)

    #     crew = Crew.objects.create(owned_by=self.user, name=self.crew_name)
    #     # Update Crew
    #     other_name = "Something Different"
    #     self.client.patch(
    #         self.edit_url + "{}/".format(crew.pk),
    #         {"name": other_name, "members": [
    #             self.friend.pk, self.other_friend.pk]},
    #     )
    #     crew.refresh_from_db()
    #     self.assertTrue(self.friend in crew.members.all())
    #     self.assertTrue(self.other_friend in crew.members.all())

    #     # Assert removing user from list of users removes them from crew
    #     self.client.patch(
    #         self.edit_url + "{}/".format(crew.pk),
    #         {"name": other_name, "members": [self.friend.pk]},
    #     )
    #     crew.refresh_from_db()
    #     self.assertTrue(self.friend in crew.members.all())
    #     self.assertFalse(self.other_friend in crew.members.all())

    #     # Clean up
    #     crew.delete()

    # def test_crew_delete_view(self):
    #     # Assert no crews right now
    #     self.assertEqual(self.user.crews_owned.count(), 0)

    #     # Set up a crew
    #     crew = Crew.objects.create(owned_by=self.user, name=self.crew_name)
    #     crew.save()
    #     crew.members.add(self.friend)
    #     self.assertEqual(self.user.crews_owned.count(), 1)

    #     # Delete crew
    #     response = self.client.delete(self.edit_url + "{}/".format(crew.pk))
    #     self.assertEqual(response.status_code, 204)
    #     self.assertEqual(self.user.crews_owned.count(), 0)

    #     # Can't delete a crew that's not owned by me
    #     crew = Crew.objects.create(owned_by=self.friend, name=self.crew_name)
    #     crew.save()
    #     crew_pk = crew.pk
    #     crew.members.add(self.user)
    #     self.assertEqual(response.status_code, 204)
    #     self.assertTrue(Crew.objects.filter(pk=crew_pk).exists())

    #     # Clean up
    #     crew.delete()
