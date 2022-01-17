from django.urls import include, path, re_path

from .views import (
    EventCreateAPIView,
    EventUpdateAPIView,
    EventResponseCreateAPIView,
    EventResponseUpdateAPIView,
    NewsFeedHomeAPIView,
)

urlpatterns = [
    path("feed/home", NewsFeedHomeAPIView.as_view(), name="newsfeed-home"),
    path("events", EventCreateAPIView.as_view(), name="event-create"),
    path(
        "events/<int:pk>", EventUpdateAPIView.as_view(), name="event-view-update-delete"
    ),
    path(
        "events/<int:event_pk>/responses",
        EventResponseCreateAPIView.as_view(),
        name="event-response-create",
    ),
    path(
        "events/<int:event_pk>/responses/<int:pk>",
        EventResponseUpdateAPIView.as_view(),
        name="event-response-view-update-delete",
    ),
]
