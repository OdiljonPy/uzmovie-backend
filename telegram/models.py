from django.db import models
from .validators import validate_username


class TelegramUser(models.Model):
    username = models.CharField(max_length=50, validators=[validate_username])
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    balance = models.IntegerField(default=0)
    is_subscribed = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username
