import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50, blank=True)
    is_verified = models.BooleanField(default=False)

    profile_picture = models.ImageField(upload_to='profile_pictures', blank=True)

    def __str__(self):
        return self.username



class OTP_code_save(models.Model):
    otp = models.IntegerField(unique=True)
    username = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True, blank=True)
    otp_key = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


