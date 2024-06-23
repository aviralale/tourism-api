from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Event(models.Model):
    event_manager = models.ForeignKey("accounts.EventManager", on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    photo1 = models.ImageField(
        upload_to="events/", null=True, blank=True, default="events/default.jpg"
    )
    photo2 = models.ImageField(
        upload_to="events/", null=True, blank=True, default="events/default.jpg"
    )
    photo3 = models.ImageField(
        upload_to="events/", null=True, blank=True, default="events/default.jpg"
    )
    video_file = models.FileField(upload_to="events/videos/", null=True, blank=True)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return self.title


class EventCompleted(models.Model):
    tourist = models.ForeignKey("accounts.Tourist", on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    event_manager = models.ForeignKey("accounts.EventManager", on_delete=models.CASCADE)
    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tourist} completed {self.event} with {self.event_manager}"


@receiver(post_save, sender=EventCompleted)
def update_num_events_handled(sender, instance, created, **kwargs):
        event_manager = instance.event_manager
        event_manager.num_of_events = (
            EventCompleted.objects.filter(event_manager=event_manager)
            .distinct("event")
            .count()
        )
        event_manager.save()
