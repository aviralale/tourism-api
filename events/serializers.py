from rest_framework import serializers
from events.models import Event, EventCompleted
from accounts.models import (
    CustomUserProfile,
    EventManagerRating,
)  # Import the model instead of the serializer


class EventManagerRatingSerializer(serializers.ModelSerializer):
    eventmanager = serializers.PrimaryKeyRelatedField(
        queryset=CustomUserProfile.objects.all()
    )
    tourist = serializers.PrimaryKeyRelatedField(
        queryset=CustomUserProfile.objects.all()
    )

    class Meta:
        model = EventManagerRating
        fields = ["id", "eventmanager", "tourist", "value"]


class EventSerializer(serializers.ModelSerializer):
    event_manager = serializers.PrimaryKeyRelatedField(
        queryset=CustomUserProfile.objects.all()
    )

    class Meta:
        model = Event
        fields = [
            "id",
            "event_manager",
            "title",
            "photo1",
            "photo2",
            "photo3",
            "video_file",
            "description",
            "start_date",
            "end_date",
        ]


class EventCompletedSerializer(serializers.ModelSerializer):
    tourist = serializers.PrimaryKeyRelatedField(
        queryset=CustomUserProfile.objects.all()
    )
    event = EventSerializer()
    event_manager = serializers.PrimaryKeyRelatedField(
        queryset=CustomUserProfile.objects.all()
    )

    class Meta:
        model = EventCompleted
        fields = ["id", "tourist", "event", "event_manager", "completed_at"]
