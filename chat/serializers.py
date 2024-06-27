from rest_framework import serializers
from .models import Conversation
from accounts.models import CustomUser


class ConversationSerializer(serializers.ModelSerializer):
    user_message = serializers.SerializerMethodField()
    ai_response = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ["user_message", "ai_response", "timestamp"]

    def get_user_message(self, obj):
        return obj.get_decrypted_user_message()

    def get_ai_response(self, obj):
        return obj.get_decrypted_ai_response()


class UserGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["email", "first_name", "last_name", "id", "username", "pfp"]
        extra_kwargs = {"id": {"read_only": True}}
