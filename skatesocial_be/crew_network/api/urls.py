from django.urls import include, path, re_path
from .views import (
    FriendRequestCreateAPIView,
    FriendRequestRespondAPIView,
    FriendRequestCancelAPIView,
    UnfriendAPIView,
    FriendListAPIView,
    CrewListAPIView,
    CrewCreateAPIView,
    CrewRetrieveUpdateDestroyAPIView,
)

urlpatterns = [
    path("friends/list/", FriendListAPIView.as_view(), name="my-friend"),
    path(
        "friends/add/<int:pk>/", FriendRequestCreateAPIView.as_view(), name="add-friend"
    ),
    path(
        "friends/remove/<int:pk>/",
        UnfriendAPIView.as_view(),
        name="remove-friend",
    ),
    path(
        "friend-request/respond/<int:pk>/",
        FriendRequestRespondAPIView.as_view(),
        name="friend-request-respond",
    ),
    path(
        "friend-request/cancel/<int:pk>/",
        FriendRequestCancelAPIView.as_view(),
        name="friend-request-cancel",
    ),
    path("crews/list/", CrewListAPIView.as_view(), name="crew-list"),
    path("crew/create/", CrewCreateAPIView.as_view(), name="create-crew"),
    path(
        "crew/edit/<int:pk>/",
        CrewRetrieveUpdateDestroyAPIView.as_view(),
        name="edit-crew",
    ),
]
