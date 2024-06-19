from rest_framework import serializers
from .models import (
    CustomUser,
    CustomUserProfile,
    Tourist,
    Guide,
    GuideRating,
    EventManager,
    EventManagerRating,
)
from events.serializers import EventManagerRatingSerializer
from tours.serializers import GuideRatingSerializer


class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=8)

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


class CustomUserProfileSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    is_guide = serializers.BooleanField(default=False)
    is_event_manager = serializers.BooleanField(default=False)

    class Meta:
        model = CustomUserProfile
        fields = ["id", "user", "is_guide", "is_event_manager"]

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user_serializer = CustomUserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()
        user_profile = CustomUserProfile.objects.create(user=user, **validated_data)
        if validated_data.get("is_guide"):
            Guide.objects.create(user_profile=user_profile)
        if validated_data.get("is_event_manager"):
            EventManager.objects.create(user_profile=user_profile)
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


class TouristSerializer(serializers.ModelSerializer):
    user_profile = CustomUserProfileSerializer()

    class Meta:
        model = Tourist
        fields = ["id", "user_profile"]

    def create(self, validated_data):
        user_profile_data = validated_data.pop("user_profile")
        user_profile_serializer = CustomUserProfileSerializer(data=user_profile_data)
        user_profile_serializer.is_valid(raise_exception=True)
        user_profile = user_profile_serializer.save()
        return Tourist.objects.create(user_profile=user_profile)

    def update(self, instance, validated_data):
        user_profile_data = validated_data.pop("user_profile")
        user_profile_serializer = CustomUserProfileSerializer(
            instance.user_profile, data=user_profile_data
        )
        user_profile_serializer.is_valid(raise_exception=True)
        user_profile_serializer.save()
        return instance


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
