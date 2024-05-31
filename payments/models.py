import uuid

from django.db import models
from authentication.models import User
from authentication.utils import generate_otp_code

from payments.utils import (
    validate_pan, validate_expire_month, validate_expire_year,
    validated_uz_phone_number,
)



from django.core.exceptions import ValidationError
from .utils import validate_pan, validate_expire_month, validate_expire_year, validated_uz_phone_number

DefaultStatuses = (
    (1, "active"),
    (1, "expired"),
    (1, "canceled"),
)


class Choice(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    description = models.TextField(max_length=260, blank=True, null=True)

    def __str__(self):
        return self.name


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    status = models.TextField(max_length=20, choices=DefaultStatuses)
    start_date = models.DateField(default=timezone.now(), null=True)
    expired_at = models.DateField(null=True)



class ChoiceOTP(models.Model):
    otp_key = models.UUIDField(default=uuid.uuid4)
    otp_code = models.IntegerField(default=generate_otp_code)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    phone_number = models.ForeignKey(User, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)




class Balance_service(models.Model):
    invoice_number = models.IntegerField()
    balance = models.IntegerField(default=0)



class Card(models.Model):
    pan = models.IntegerField(max_length=16, validators=[validate_pan])
    expire_month = models.IntegerField(max_length=2, validators=[validate_expire_month])
    expire_year = models.IntegerField(max_length=4, validators=[validate_expire_year])



class Cards(models.Model):
    pan = models.IntegerField(default=0, validators=[validate_pan])
    expire_month = models.IntegerField(default=0, validators=[validate_expire_month])
    expire_year = models.IntegerField(default=0, validators=[validate_expire_year])



    holder_full_name = models.CharField(max_length=120)
    phone_number = models.ForeignKey(User, on_delete=models.CASCADE)
    balance = models.IntegerField(default=0)

    token = models.UUIDField(default=uuid.uuid4, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.holder_full_name
