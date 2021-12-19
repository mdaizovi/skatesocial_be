from django.urls import include, path, re_path
from .views import FriendRequestCreateView, FriendRequestRespondView

urlpatterns = [
    # path("add-friend/", FriendRequestCreateView.as_view(), name="add-friend"),
    path("add-friend/<int:pk>/", FriendRequestCreateView.as_view(), name="add-friend"),
    path(
        "friend-request-respond/<int:pk>/",
        FriendRequestRespondView.as_view(),
        name="friend-request-respond",
    ),
    #     path(
    #     "friend-request-cancel/<int:pk>/",
    #     FriendRequestCancelView.as_view(),
    #     name="friend-request-cancel",
    # ),
    #     path(
    #     "remove-friend/<int:pk>/",
    #     FriendRemoveView.as_view(),
    #     name="remove-friend",
    # ),
]
