from rest_framework import serializers
from .models import Conversation

class ConversationSerializer(serializers.ModelSerializer):
    user_message = serializers.SerializerMethodField()
    ai_response = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['user_message', 'ai_response', 'timestamp']

    def get_user_message(self, obj):
        return obj.get_decrypted_user_message()

    def get_ai_response(self, obj):
        return obj.get_decrypted_ai_response()
