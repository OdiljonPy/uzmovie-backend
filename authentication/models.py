import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from .utils import username_validation, generate_otp_code


OtpTypes = (
    (1, "register"),
    (2, 'resend')
)


class User(AbstractUser):
    username = models.CharField(
        max_length=12,
        unique=True,
        help_text=(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validation],
        error_messages={
            "unique": "A user with that username already exists.",
        },
    )

    is_verified = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to='profile_pictures', blank=True, null=True)

    def __str__(self):
        return self.username


class OTPRegisterResend(models.Model):
    otp_key = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    otp_code = models.PositiveIntegerField(default=generate_otp_code)

    otp_user = models.ForeignKey(User, models.SET_NULL, null=True)
    otp_type = models.IntegerField(choices=OtpTypes, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.created_at)


