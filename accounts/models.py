from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
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
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=254, unique=True)
    username = models.CharField(max_length=150, unique=True, default=uuid.uuid1)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    pfp = models.ImageField(upload_to='user_avatar/', null=True, blank=True, default='user_avatar/default.jpg')
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return self.username

class CustomUserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    rating = models.FloatField(default=0.0)
    is_guide = models.BooleanField(default=False)

    def set_as_guide(self):
        self.is_guide = True
        self.save()
        Guide.objects.create(user_profile=self)

    def set_as_tourist(self):
        self.is_guide = False
        self.save()
        Tourist.objects.create(user_profile=self)

class Tourist(models.Model):
    user_profile = models.OneToOneField(CustomUserProfile, on_delete=models.CASCADE)
    # Additional fields for tourists

class Guide(models.Model):
    user_profile = models.OneToOneField(CustomUserProfile, on_delete=models.CASCADE)
    num_tourists_handled = models.IntegerField(default=0)
    # Additional fields for guides
