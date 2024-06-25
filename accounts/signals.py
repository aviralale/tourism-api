from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db import transaction
from .models import CustomUserProfile, Guide, EventManager, Tourist

@receiver(post_save, sender=CustomUserProfile)
def create_or_update_profile_related_models(sender, instance, created, **kwargs):
    if created:
        if instance.user.is_guide:
            Guide.objects.create(user_profile=instance)
        elif instance.user.is_event_manager:
            EventManager.objects.create(user_profile=instance)
        else:
            Tourist.objects.create(user_profile=instance)

@receiver(post_delete, sender=CustomUserProfile)
def delete_profile_related_models(sender, instance, **kwargs):
    try:
        guide = Guide.objects.get(user_profile=instance)
        guide.delete()
    except Guide.DoesNotExist:
        pass
        
    try:
        event_manager = EventManager.objects.get(user_profile=instance)
        event_manager.delete()
    except EventManager.DoesNotExist:
        pass
        
    try:
        tourist = Tourist.objects.get(user_profile=instance)
        tourist.delete()
    except Tourist.DoesNotExist:
        pass
