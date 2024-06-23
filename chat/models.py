from django.db import models
from cryptography.fernet import Fernet
from django.conf import settings
from accounts.models import CustomUser
# Ensure you generate and store a secure key in your settings
settings.SECRET_KEY = Fernet.generate_key()

def encrypt_text(plain_text):
    f = Fernet(settings.SECRET_KEY)
    return f.encrypt(plain_text.encode()).decode()

def decrypt_text(encrypted_text):
    f = Fernet(settings.SECRET_KEY)
    return f.decrypt(encrypted_text.encode()).decode()

class Conversation(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    user_message = models.TextField()
    ai_response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.user_message = encrypt_text(self.user_message)
        self.ai_response = encrypt_text(self.ai_response)
        super().save(*args, **kwargs)

    def get_decrypted_user_message(self):
        return decrypt_text(self.user_message)

    def get_decrypted_ai_response(self):
        return decrypt_text(self.ai_response)
