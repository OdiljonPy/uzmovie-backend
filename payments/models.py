import uuid
from django.db import models
from authentication.models import User
from authentication.utils import generate_otp_code


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





