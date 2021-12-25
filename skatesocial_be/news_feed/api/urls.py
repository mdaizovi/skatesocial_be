from django.urls import include, path, re_path

from .views import EventCreateAPIView, EventUpdateAPIView

urlpatterns = [
    path("event/create/", EventCreateAPIView.as_view(), name="event-create"),
    path("event/edit/<int:pk>/", EventUpdateAPIView.as_view(), name="event-edit"),
    # path("event/<int:pk>/", RegisterView.as_view(), name="event-view"),
    # list of events i can see? i guess that's the newsfeed itself.
    # path("event_response/create", RegisterView.as_view(), name="event-response-create"),
    # path("event_response/edit/<int:pk>/", RegisterView.as_view(), name="event-response-edit"),
]
