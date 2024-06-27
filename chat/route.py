from django.urls import path
from .consumers import PersonalChatConsumer

websocket_patterns = [
    path("ws/chat/<int:id>/", PersonalChatConsumer.as_asgi()),
]
