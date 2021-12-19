from django.urls import include, path, re_path
from .views import FriendRequestCreateView, FriendRequestRespondView

urlpatterns = [
    path("add-friend/", FriendRequestCreateView.as_view(), name="add-friend"),
    path(
        "friend-request-respond/",
        FriendRequestRespondView.as_view(),
        name="friend-request-respond",
    ),
]
