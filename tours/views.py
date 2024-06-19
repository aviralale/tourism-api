from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializers import TourSerializer, TouristCompletedTourSerializer
from .models import Tour, TouristCompletedTour


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
