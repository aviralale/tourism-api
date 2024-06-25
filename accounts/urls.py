from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import SignupView, UserProfileView, GuideView, TouristView, EventManagerView, LogoutView, CurrentUserView

urlpatterns = [
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("signup/", SignupView.as_view(), name="signup"),
    path('me/', CurrentUserView.as_view(), name='current_user'),
    path("profile/<str:username>/", UserProfileView.as_view(), name="profile"),
    path("guides/", GuideView.as_view(), name="guides-list"),
    path("guides/<int:pk>/", GuideView.as_view(), name="guide-detail"),
    path("tourists/", TouristView.as_view(), name="tourists-list"),
    path("tourists/<int:pk>/", TouristView.as_view(), name="tourist-detail"),
    path("event-managers/", EventManagerView.as_view(), name="event-managers-list"),
    path("event-managers/<int:pk>/", EventManagerView.as_view(), name="event-manager-detail"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
