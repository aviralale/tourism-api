from django.urls import path

from .views import TourView, TouristCompletedTourView

urlpatterns = [
    path("", TourView.as_view(), name="tours-list"),
    path("tours/<int:pk>/", TourView.as_view(), name="tour-detail"),
    path(
        "completed-tours/",
        TouristCompletedTourView.as_view(),
        name="completed-tours-list",
    ),
    path(
        "completed-tours/<int:pk>/",
        TouristCompletedTourView.as_view(),
        name="completed-tour-detail",
    ),
]
