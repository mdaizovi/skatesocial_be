from django.urls import include, path, re_path
from .views import (
    FriendRequestCreateAPIView,
    FriendRequestRespondCancelAPIView,
    UnfriendAPIView,
    FriendListAPIView,
    CrewAPIView,
    CrewRetrieveUpdateDestroyAPIView,
)

urlpatterns = [
    path("friends", FriendListAPIView.as_view(), name="my-friends"),
    path(
        "friends/<int:pk>",
        UnfriendAPIView.as_view(),
        name="remove-friend",
    ),
    path(
        "friends/requests", FriendRequestCreateAPIView.as_view(), name="add-friend"
    ),  # POST only, with target in POST.
    path(
        "friends/requests/<int:pk>",
        FriendRequestRespondCancelAPIView.as_view(),
        name="friend-request-action",
    ),  # DEL to cancel one you started, PATCH to respond to one towards you
    # GET to view a list of my crews, POST to create a crew
    path("crews", CrewAPIView.as_view(), name="crew-list-or-create"),
    path(
        "crews/<int:pk>",
        CrewRetrieveUpdateDestroyAPIView.as_view(),
        name="edit-crew",  # PATCH or #DELETE
    ),
]
