import uuid
from django.db import models
from authentication.models import User
from authentication.utils import generate_otp_code, username_validation
from .utils import validate_pan, validate_expire_month, validate_expire_year
from django.utils import timezone

DefaultStatuses = (
    (1, "active"),
    (2, "expired"),
    (3, "canceled"),
)


class Choice(models.Model):
    name = models.CharField(max_length=100)
    price = models.PositiveIntegerField(default=0)
    description = models.TextField(max_length=260, blank=True, null=True)
    deleted_at = models.DateField(null=True)

    def __str__(self):
        return self.name


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    status = models.TextField(max_length=20, choices=DefaultStatuses)
    start_date = models.DateField(default=timezone.now, null=True)
    expired_at = models.DateField(null=True)

    deleted_at = models.DateTimeField(null=True)

    def __str__(self):
        return self.user.username


class ChoiceOTP(models.Model):
    otp_key = models.UUIDField(default=uuid.uuid4)
    otp_code = models.IntegerField(default=generate_otp_code)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_number = models.IntegerField(validators=[username_validation])

    created_at = models.DateTimeField(auto_now_add=True)

    deleted_at = models.DateTimeField(null=True)

    def __str__(self):
        return self.user.username


class Card(models.Model):
    pan = models.IntegerField(validators=[validate_pan])
    expire_month = models.IntegerField(validators=[validate_expire_month])
    expire_year = models.IntegerField(validators=[validate_expire_year])

    holder_full_name = models.CharField(max_length=120)
    phone_number = models.CharField(max_length=12, validators=[username_validation])
    balance = models.PositiveIntegerField(default=0)

    token = models.UUIDField(default=uuid.uuid4, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateField(null=True)

    def __str__(self):
        return self.holder_full_name
