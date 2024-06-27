from django.urls import path
from . import views

urlpatterns = [
    path("", views.chat_page, name="chat_page"),
    path("main_processor/", views.main_processor, name="main_processor"),
    path("get_conversations/", views.get_conversations, name="get_conversations"),
    path("users/", views.get_user_list, name="users"),
]
