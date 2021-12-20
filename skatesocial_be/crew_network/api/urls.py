from django.urls import include, path, re_path
from .views import (
    FriendRequestCreateView,
    FriendRequestRespondView,
    FriendRequestCancelView,
    UnfriendView,
    FriendListView,
)

urlpatterns = [
    path("friends/list/", FriendListView.as_view(), name="my-friend"),
    path("friends/add/<int:pk>/", FriendRequestCreateView.as_view(), name="add-friend"),
    path(
        "friends/remove/<int:pk>/",
        UnfriendView.as_view(),
        name="remove-friend",
    ),
    path(
        "friend-request/respond/<int:pk>/",
        FriendRequestRespondView.as_view(),
        name="friend-request-respond",
    ),
    path(
        "friend-request/cancel/<int:pk>/",
        FriendRequestCancelView.as_view(),
        name="friend-request-cancel",
    ),
]
