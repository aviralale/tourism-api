from django.shortcuts import render
import google.ai.generativelanguage as glm
import google.generativeai as genai
import io
from PIL import Image
from django.http import JsonResponse
from .models import Conversation
from .serializers import ConversationSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import markdown
from accounts.models import CustomUser
from .serializers import UserGetSerializer

GOOGLE_API_KEY = "AIzaSyDCn8O8RvEC-4iokxfm8g_4dJ9VRP260Io"
genai.configure(api_key=GOOGLE_API_KEY)

# Create your views here.


def chat_page(request, *args, **kwargs):
    return render(request, "index.html")


def to_markdown(text):
    return markdown.markdown(text)


@api_view(["POST"])
def main_processor(request, *args, **kwargs):
    text_data = request.data.get("text")
    file_data = request.FILES.get("file")
    parts = []
    g_mode = "gemini-pro"

    if file_data is not None:
        g_mode += "-vision"
        image_file = file_data.read()
        with io.BytesIO(image_file) as img_io:
            img = Image.open(img_io)
            image_format = img.format

        # Get MIME type and extension
        mime = f"image/{image_format.lower()}"

        parts.append(glm.Part(inline_data=glm.Blob(mime_type=mime, data=image_file)))

    if text_data:
        parts.append(glm.Part(text=text_data))

    model = genai.GenerativeModel(g_mode)
    response = model.generate_content(glm.Content(parts=parts))

    ai_response_text = to_markdown(response.parts[0].text)

    # Save the conversation to the database
    conversation = Conversation.objects.create(
        user_message=text_data, ai_response=ai_response_text
    )

    response_data = {"response": ai_response_text}

    return JsonResponse(response_data)


@api_view(["GET"])
def get_conversations(request, *args, **kwargs):
    conversations = Conversation.objects.all().order_by("-timestamp")
    serializer = ConversationSerializer(conversations, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_list(request):
    try:
        user_obj = CustomUser.objects.exclude(id=request.user.id)
        serializer = UserGetSerializer(user_obj, many=True)
        return Response(serializer.data)
    except Exception as e:
        print("Error in getting users list", str(e))
        return Response({"error": "Error in getting user list"}, status=400)
