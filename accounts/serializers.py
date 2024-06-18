from rest_framework import serializers
from .models import CustomUser, CustomUserProfile, Tourist, Guide
import uuid

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 'is_active', 'is_staff', 'created_at', 'pfp', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_password(self, value):
        if not value:
            raise serializers.ValidationError("Password is required.")
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser(
            email=validated_data['email'],
            username=validated_data.get('username', str(uuid.uuid1())),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            pfp=validated_data.get('pfp', 'user_avatar/default.jpg')
        )
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
        instance.pfp = validated_data.get('pfp', instance.pfp)
        instance.save()
        return instance

class CustomUserProfileSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    is_guide = serializers.BooleanField()

    class Meta:
        model = CustomUserProfile
        fields = ['id', 'user', 'rating', 'is_guide']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_serializer = CustomUserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()
        user_profile = CustomUserProfile.objects.create(user=user, **validated_data)
        if validated_data['is_guide']:
            user_profile.set_as_guide()
        else:
            user_profile.set_as_tourist()
        return user_profile

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        user = instance.user

        user_serializer = CustomUserSerializer(user, data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()

        instance.rating = validated_data.get('rating', instance.rating)
        is_guide = validated_data.get('is_guide', instance.is_guide)

        if is_guide != instance.is_guide:
            if is_guide:
                instance.set_as_guide()
            else:
                instance.set_as_tourist()

        instance.save()
        return instance

class TouristSerializer(serializers.ModelSerializer):
    user_profile = CustomUserProfileSerializer()

    class Meta:
        model = Tourist
        fields = ['id', 'user_profile']

class GuideSerializer(serializers.ModelSerializer):
    user_profile = CustomUserProfileSerializer()

    class Meta:
        model = Guide
        fields = ['id', 'user_profile', 'num_tourists_handled']
