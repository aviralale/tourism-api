from django.urls import path

from .views import (
    EventView,
    EventCompletedView,
)

urlpatterns = [
    path("", EventView.as_view(), name="events-list"),
    path("events/<int:pk>/", EventView.as_view(), name="event-detail"),
    path(
        "completed-events/", EventCompletedView.as_view(), name="completed-events-list"
    ),
    path(
        "completed-events/<int:pk>/",
        EventCompletedView.as_view(),
        name="completed-event-detail",
    ),
]
