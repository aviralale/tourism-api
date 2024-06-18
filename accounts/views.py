from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import (
    CustomUserProfile,
    Guide,
    Tourist,
    EventManager,
    Tour,
    TouristCompletedTour,
    Event,
    EventCompleted,
)
from .serializers import (
    CustomUserSerializer,
    CustomUserProfileSerializer,
    TouristSerializer,
    GuideSerializer,
    GuideRatingSerializer,
    EventManagerSerializer,
    EventManagerRatingSerializer,
    TourSerializer,
    TouristCompletedTourSerializer,
    EventSerializer,
    EventCompletedSerializer,
)


# User Signup View
class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = CustomUserProfileSerializer(data=request.data)
        if serializer.is_valid():
            user_profile = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# User Profile View
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_profile = CustomUserProfile.objects.get(user=request.user)
        serializer = CustomUserProfileSerializer(user_profile)
        return Response(serializer.data)

    def put(self, request):
        user_profile = CustomUserProfile.objects.get(user=request.user)
        serializer = CustomUserProfileSerializer(
            user_profile, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Guide View
class GuideView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk:
            guide = Guide.objects.get(pk=pk)
            serializer = GuideSerializer(guide)
        else:
            guides = Guide.objects.all()
            serializer = GuideSerializer(guides, many=True)
        return Response(serializer.data)


# Tourist View
class TouristView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk:
            tourist = Tourist.objects.get(pk=pk)
            serializer = TouristSerializer(tourist)
        else:
            tourists = Tourist.objects.all()
            serializer = TouristSerializer(tourists, many=True)
        return Response(serializer.data)


# Event Manager View
class EventManagerView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk:
            event_manager = EventManager.objects.get(pk=pk)
            serializer = EventManagerSerializer(event_manager)
        else:
            event_managers = EventManager.objects.all()
            serializer = EventManagerSerializer(event_managers, many=True)
        return Response(serializer.data)


# Tour View
class TourView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk:
            tour = Tour.objects.get(pk=pk)
            serializer = TourSerializer(tour)
        else:
            tours = Tour.objects.all()
            serializer = TourSerializer(tours, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TourSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Tourist Completed Tour View
class TouristCompletedTourView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk:
            completed_tour = TouristCompletedTour.objects.get(pk=pk)
            serializer = TouristCompletedTourSerializer(completed_tour)
        else:
            completed_tours = TouristCompletedTour.objects.all()
            serializer = TouristCompletedTourSerializer(completed_tours, many=True)
        return Response(serializer.data)


# Event View
class EventView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk:
            event = Event.objects.get(pk=pk)
            serializer = EventSerializer(event)
        else:
            events = Event.objects.all()
            serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Event Completed View
class EventCompletedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk:
            completed_event = EventCompleted.objects.get(pk=pk)
            serializer = EventCompletedSerializer(completed_event)
        else:
            completed_events = EventCompleted.objects.all()
            serializer = EventCompletedSerializer(completed_events, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = EventCompletedSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
