from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=254, unique=True)
    username = models.CharField(max_length=150, unique=True, default=uuid.uuid1)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    pfp = models.ImageField(
        upload_to="user_avatar/",
        null=True,
        blank=True,
        default="user_avatar/default.jpg",
    )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    def __str__(self):
        return self.username


class CustomUserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    is_guide = models.BooleanField(default=False)
    is_event_manager = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


@receiver(post_save, sender=CustomUserProfile)
def create_guide_instance(sender, instance, created, **kwargs):
    if created and instance.is_guide:
        Guide.objects.create(user_profile=instance)


@receiver(post_save, sender=CustomUserProfile)
def update_guide_instance(sender, instance, **kwargs):
    try:
        guide = Guide.objects.get(user_profile=instance)
        if not instance.is_guide:
            guide.delete()
    except Guide.DoesNotExist:
        if instance.is_guide:
            Guide.objects.create(user_profile=instance)


class Tourist(models.Model):
    user_profile = models.OneToOneField(CustomUserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user_profile.user.first_name} {self.user_profile.user.last_name}"


class Guide(models.Model):
    user_profile = models.OneToOneField(CustomUserProfile, on_delete=models.CASCADE)
    num_tourists_handled = models.IntegerField(default=0)

    @property
    def average_rating(self):
        ratings = self.ratings.all()
        if ratings.exists():
            return sum(rating.value for rating in ratings) / ratings.count()
        return 0.0

    def __str__(self):
        return f"Guide: {self.user_profile.user.first_name} {self.user_profile.user.last_name}"




class EventManager(models.Model):
    user_profile = models.OneToOneField(CustomUserProfile, on_delete=models.CASCADE)
    num_of_events = models.IntegerField(default=0)

    @property
    def average_rating(self):
        ratings = self.ratings.all()
        if ratings.exists():
            return sum(rating.value for rating in ratings) / ratings.count()
        return 0.0

    def __str__(self):
        return f"EventManager: {self.user_profile.user.first_name} {self.user_profile.user.last_name}"



class Tour(models.Model):
    guide = models.ForeignKey(Guide, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return self.title


class TouristCompletedTour(models.Model):
    tourist = models.ForeignKey(Tourist, on_delete=models.CASCADE)
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    guide = models.ForeignKey(Guide, on_delete=models.CASCADE,  null=True)
    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tourist} completed {self.tour}"


@receiver(post_save, sender=TouristCompletedTour)
def update_num_tourists_handled(sender, instance, created, **kwargs):
    if created:
        guide = instance.tour.guide
        guide.num_tourists_handled = (
            TouristCompletedTour.objects.filter(tour__guide=guide)
            .distinct("tourist")
            .count()
        )
        guide.save()


class Event(models.Model):
    event_manager = models.ForeignKey(EventManager, on_delete=models.CASCADE)
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
    tourist = models.ForeignKey(Tourist, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    event_manager = models.ForeignKey(EventManager, on_delete=models.CASCADE)
    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tourist} completed {self.event} with {self.event_manager}"


@receiver(post_save, sender=EventCompleted)
def update_num_events_handled(sender, instance, created, **kwargs):
    if created:
        event_manager = instance.event_manager
        event_manager.num_of_events = (
            EventCompleted.objects.filter(event_manager=event_manager)
            .distinct("event")
            .count()
        )
        event_manager.save()

class EventManagerRating(models.Model):
    eventmanager = models.ForeignKey(EventManager, related_name="ratings", on_delete=models.CASCADE)
    tourist = models.ForeignKey(Tourist, on_delete=models.CASCADE)
    event = models.ForeignKey(EventCompleted, on_delete=models.CASCADE)
    value = models.FloatField()

    def __str__(self):
        return f"Rating {self.value} for {self.guide} by {self.tourist}"
class GuideRating(models.Model):
    guide = models.ForeignKey(Guide, related_name="ratings", on_delete=models.CASCADE)
    tourist = models.ForeignKey(Tourist, on_delete=models.CASCADE)
    tour = models.ForeignKey(TouristCompletedTour, on_delete=models.CASCADE, null=True)
    value = models.FloatField()

    def __str__(self):
        return f"Rating {self.value} for {self.guide} by {self.tourist}"