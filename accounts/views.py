from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from .models import (
    CustomUserProfile,
    Guide,
    Tourist,
    EventManager,
)
from .serializers import (
    CustomUserProfileSerializer,
    TouristSerializer,
    GuideSerializer,
    EventManagerSerializer,
)


class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        user_data = {
            "user": {
                "email": request.data.get("email"),
                "username": request.data.get("username"),
                "first_name": request.data.get("first_name"),
                "last_name": request.data.get("last_name"),
                "password": request.data.get("password"),
                "pfp": request.data.get("pfp", "user_avatar/default.jpg"),
            },
            "is_guide": request.data.get("is_guide", False),
            "is_event_manager": request.data.get("is_event_manager", False),
        }
        serializer = CustomUserProfileSerializer(data=user_data)
        if serializer.is_valid():
            user_profile = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)  # Log errors to console
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh_token')
            if not refresh_token:
                return Response({'error': 'refresh_token is required'}, status=status.HTTP_400_BAD_REQUEST)

            # Blacklist the refresh token to invalidate it
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({'message': 'Logout successful.'}, status=status.HTTP_200_OK)

        except TokenError as e:
            return Response({'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
