from rest_framework import serializers
from accounts.models import CustomUserProfile, GuideRating
from .models import Tour, TouristCompletedTour


class GuideSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUserProfile
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
        ]  # Adjust fields as per your model


class GuideRatingSerializer(serializers.ModelSerializer):
    guide = serializers.PrimaryKeyRelatedField(queryset=CustomUserProfile.objects.all())
    tourist = serializers.PrimaryKeyRelatedField(
        queryset=CustomUserProfile.objects.all()
    )

    class Meta:
        model = GuideRating
        fields = ["id", "guide", "tourist", "value"]

    def validate(self, attrs):
        guide = attrs.get("guide")
        tourist = attrs.get("tourist")

        if guide == tourist:
            raise serializers.ValidationError("Guide and tourist cannot be the same.")

        return attrs


class TourSerializer(serializers.ModelSerializer):
    guide = GuideSerializer()

    class Meta:
        model = Tour
        fields = ["id", "guide", "title", "description", "start_date", "end_date"]

    def validate(self, attrs):
        start_date = attrs.get("start_date")
        end_date = attrs.get("end_date")

        if start_date and end_date and start_date >= end_date:
            raise serializers.ValidationError("End date must be after start date.")

        return attrs


class TouristCompletedTourSerializer(serializers.ModelSerializer):
    tourist = serializers.PrimaryKeyRelatedField(
        queryset=CustomUserProfile.objects.all()
    )
    tour = serializers.PrimaryKeyRelatedField(queryset=Tour.objects.all())
    guide = serializers.PrimaryKeyRelatedField(queryset=CustomUserProfile.objects.all())

    class Meta:
        model = TouristCompletedTour
        fields = ["id", "tourist", "tour", "guide", "completed_at"]

    def create(self, validated_data):
        tourist_data = validated_data.pop("tourist")
        tour_data = validated_data.pop("tour")
        guide_data = validated_data.pop("guide")

        tourist_serializer = TouristSerializer(data=tourist_data)
        tourist_serializer.is_valid(raise_exception=True)
        tourist_instance = tourist_serializer.save()

        tour_instance = Tour.objects.create(**tour_data, guide=guide_data)

        return TouristCompletedTour.objects.create(
            tourist=tourist_instance,
            tour=tour_instance,
            guide=guide_data,
            **validated_data
        )

    def update(self, instance, validated_data):
        tourist_data = validated_data.pop("tourist")
        tour_data = validated_data.pop("tour")
        guide_data = validated_data.pop("guide")

        tourist_serializer = TouristSerializer(instance.tourist, data=tourist_data)
        tourist_serializer.is_valid(raise_exception=True)
        tourist_instance = tourist_serializer.save()

        tour_instance = instance.tour
        for attr, value in tour_data.items():
            setattr(tour_instance, attr, value)
        tour_instance.guide = guide_data
        tour_instance.save()

        instance.completed_at = validated_data.get(
            "completed_at", instance.completed_at
        )
        instance.save()

        return instance
