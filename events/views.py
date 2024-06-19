from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Event, EventCompleted

from .serializers import EventSerializer, EventCompletedSerializer
    
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
