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
    CustomUserSerializer
)
import logging

logger = logging.getLogger(__name__)

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from .models import CustomUserProfile, Guide, Tourist, EventManager
from .serializers import CustomUserProfileSerializer, TouristSerializer, GuideSerializer, EventManagerSerializer, CustomUserSerializer
import logging

logger = logging.getLogger(__name__)


class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            serializer = CustomUserSerializer(data=request.data.get("user"))
            if serializer.is_valid():
                user = serializer.save()
                # The signal will handle creation of CustomUserProfile
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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

class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        logger.debug("CurrentUserView GET request received")
        serializer = CustomUserSerializer(request.user)
        return Response(serializer.data)

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, username):
        logger.debug(f"Requested username: {username}, authenticated user: {request.user.username}")

        if request.user.username != username:
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            user_profile = CustomUserProfile.objects.get(user=request.user)
            serializer = CustomUserProfileSerializer(user_profile)
            return Response(serializer.data)
        except CustomUserProfile.DoesNotExist:
            logger.error(f"User profile not found for username: {username}")
            return Response({"error": "User profile not found."}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, username):
        logger.debug(f"Requested username: {username}, authenticated user: {request.user.username}")

        if request.user.username != username:
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            user_profile = CustomUserProfile.objects.get(user=request.user)
            serializer = CustomUserProfileSerializer(user_profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except CustomUserProfile.DoesNotExist:
            logger.error(f"User profile not found for username: {username}")
            return Response({"error": "User profile not found."}, status=status.HTTP_404_NOT_FOUND)

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

    def post(self, request):
        serializer = GuideSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        guide = Guide.objects.get(pk=pk)
        serializer = GuideSerializer(guide, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        guide = Guide.objects.get(pk=pk)
        guide.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

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

    def post(self, request):
        serializer = EventManagerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        event_manager = EventManager.objects.get(pk=pk)
        serializer = EventManagerSerializer(event_manager, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        event_manager = EventManager.objects.get(pk=pk)
        event_manager.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

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

    def post(self, request):
        serializer = TouristSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        tourist = Tourist.objects.get(pk=pk)
        serializer = TouristSerializer(tourist, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        tourist = Tourist.objects.get(pk=pk)
        tourist.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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


class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        logger.debug("CurrentUserView GET request received")
        serializer = CustomUserSerializer(request.user)
        return Response(serializer.data)

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, username):
        logger.debug(f"Requested username: {username}, authenticated user: {request.user.username}")

        if request.user.username != username:
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            user_profile = CustomUserProfile.objects.get(user=request.user)
            serializer = CustomUserProfileSerializer(user_profile)
            return Response(serializer.data)
        except CustomUserProfile.DoesNotExist:
            logger.error(f"User profile not found for username: {username}")
            return Response({"error": "User profile not found."}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, username):
        logger.debug(f"Requested username: {username}, authenticated user: {request.user.username}")

        if request.user.username != username:
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            user_profile = CustomUserProfile.objects.get(user=request.user)
            serializer = CustomUserProfileSerializer(user_profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except CustomUserProfile.DoesNotExist:
            logger.error(f"User profile not found for username: {username}")
            return Response({"error": "User profile not found."}, status=status.HTTP_404_NOT_FOUND)

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

    def post(self, request):
        serializer = GuideSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        guide = Guide.objects.get(pk=pk)
        serializer = GuideSerializer(guide, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        guide = Guide.objects.get(pk=pk)
        guide.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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

    def post(self, request):
        serializer = EventManagerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        event_manager = EventManager.objects.get(pk=pk)
        serializer = EventManagerSerializer(event_manager, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        event_manager = EventManager.objects.get(pk=pk)
        event_manager.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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

    def post(self, request):
        serializer = TouristSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        tourist = Tourist.objects.get(pk=pk)
        serializer = TouristSerializer(tourist, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        tourist = Tourist.objects.get(pk=pk)
        tourist.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
