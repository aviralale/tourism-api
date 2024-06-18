from rest_framework import serializers
from .models import (
    CustomUser,
    CustomUserProfile,
    Tourist,
    Guide,
    GuideRating,
    EventManager,
    EventManagerRating,
    Tour,
    TouristCompletedTour,
    Event,
    EventCompleted,
)


# CustomUser Serializer
class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "is_active",
            "is_staff",
            "created_at",
            "pfp",
            "password",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def validate_password(self, value):
        if not value:
            raise serializers.ValidationError("Password is required.")
        if len(value) < 8:
            raise serializers.ValidationError(
                "Password must be at least 8 characters long."
            )
        return value

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = CustomUser.objects.create_user(password=password, **validated_data)
        return user

    def update(self, instance, validated_data):
        instance.email = validated_data.get("email", instance.email)
        instance.username = validated_data.get("username", instance.username)
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        if "password" in validated_data:
            instance.set_password(validated_data["password"])
        instance.pfp = validated_data.get("pfp", instance.pfp)
        instance.save()
        return instance


# CustomUserProfile Serializer
class CustomUserProfileSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    is_guide = serializers.BooleanField()
    is_event_manager = serializers.BooleanField()

    class Meta:
        model = CustomUserProfile
        fields = ["id", "user", "is_guide", "is_event_manager"]

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user_serializer = CustomUserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()
        user_profile = CustomUserProfile.objects.create(user=user, **validated_data)
        return user_profile

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user")
        user = instance.user

        user_serializer = CustomUserSerializer(user, data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()

        instance.is_guide = validated_data.get("is_guide", instance.is_guide)
        instance.is_event_manager = validated_data.get(
            "is_event_manager", instance.is_event_manager
        )
        instance.save()
        return instance


# Tourist Serializer
class TouristSerializer(serializers.ModelSerializer):
    user_profile = CustomUserProfileSerializer()

    class Meta:
        model = Tourist
        fields = ["id", "user_profile"]


# Guide Serializer
class GuideSerializer(serializers.ModelSerializer):
    user_profile = CustomUserProfileSerializer()
    average_rating = serializers.FloatField(source="average_rating", read_only=True)
    ratings = serializers.SerializerMethodField()

    class Meta:
        model = Guide
        fields = [
            "id",
            "user_profile",
            "num_tourists_handled",
            "average_rating",
            "ratings",
        ]

    def get_ratings(self, obj):
        ratings = GuideRating.objects.filter(guide=obj)
        return GuideRatingSerializer(ratings, many=True).data


# GuideRating Serializer
class GuideRatingSerializer(serializers.ModelSerializer):
    guide = GuideSerializer()
    tourist = TouristSerializer()

    class Meta:
        model = GuideRating
        fields = ["id", "guide", "tourist", "value"]


# EventManager Serializer
class EventManagerSerializer(serializers.ModelSerializer):
    user_profile = CustomUserProfileSerializer()
    average_rating = serializers.FloatField(source="average_rating", read_only=True)
    ratings = serializers.SerializerMethodField()

    class Meta:
        model = EventManager
        fields = ["id", "user_profile", "num_of_events", "average_rating", "ratings"]

    def get_ratings(self, obj):
        ratings = EventManagerRating.objects.filter(eventmanager=obj)
        return EventManagerRatingSerializer(ratings, many=True).data


# EventManagerRating Serializer
class EventManagerRatingSerializer(serializers.ModelSerializer):
    eventmanager = EventManagerSerializer()
    tourist = TouristSerializer()

    class Meta:
        model = EventManagerRating
        fields = ["id", "eventmanager", "tourist", "value"]


# Tour Serializer
class TourSerializer(serializers.ModelSerializer):
    guide = GuideSerializer()

    class Meta:
        model = Tour
        fields = ["id", "guide", "title", "description", "start_date", "end_date"]


# TouristCompletedTour Serializer
class TouristCompletedTourSerializer(serializers.ModelSerializer):
    tourist = TouristSerializer()
    tour = TourSerializer()
    guide = GuideSerializer()

    class Meta:
        model = TouristCompletedTour
        fields = ["id", "tourist", "tour", "guide", "completed_at"]


# Event Serializer
class EventSerializer(serializers.ModelSerializer):
    event_manager = EventManagerSerializer()

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


# EventCompleted Serializer
class EventCompletedSerializer(serializers.ModelSerializer):
    tourist = TouristSerializer()
    event = EventSerializer()
    event_manager = EventManagerSerializer()

    class Meta:
        model = EventCompleted
        fields = ["id", "tourist", "event", "event_manager", "completed_at"]
