from django.urls import include, path, re_path

from .views import EventCreateAPIView, EventUpdateAPIView

urlpatterns = [
    path("events", EventCreateAPIView.as_view(), name="event-create"),
    path(
        "events/<int:pk>", EventUpdateAPIView.as_view(), name="event-view-update-delete"
    ),
    # TODO make other urls follow this best practice pattern.
    # path("events/<int:pk>/responses", RegisterView.as_view(), name="event-response-create"),
    # path("events/<int:event_pk>/responses/<int:pk>", RegisterView.as_view(), name="event-response-view-update-delete"),
]
