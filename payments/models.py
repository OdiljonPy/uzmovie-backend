import uuid
from django.db import models
from authentication.models import User
from authentication.utils import generate_otp_code
from payments.utils import validate_pan, validate_expire_month, validate_expire_year, validated_uz_phone_number


# active/expired/canceled


class Status(models.Model):
    name = models.CharField(max_length=50)


class Choice(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    description = models.TextField()

    def __str__(self):
        return self.name


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    start_date = models.DateField(null=True)
    expiring_on = models.DateField(null=True)

    def __str__(self):
        return self.user.username


class ChoiceOTP(models.Model):
    otp_key = models.UUIDField(default=uuid.uuid4)
    otp_kode = models.IntegerField(default=generate_otp_code)
    phone_number = models.CharField(max_length=12)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.phone_number

class Balance_service(models.Model):
    invoice_number = models.IntegerField()
    balance = models.IntegerField(default=0)

    def __str__(self):
        return self.balance

class Cards(models.Model):
    pan = models.IntegerField(default=0, validators=[validate_pan])
    expire_month = models.IntegerField(default=0, validators=[validate_expire_month])
    expire_year = models.IntegerField(default=0, validators=[validate_expire_year])

    holder_full_name = models.CharField(max_length=120)
    phone_number = models.CharField(max_length=12, validators=[validated_uz_phone_number])

    balance = models.IntegerField(default=0)

    token = models.UUIDField(default=uuid.uuid4, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.holder_full_name







