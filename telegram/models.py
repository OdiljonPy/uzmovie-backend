from django.db import models

from movie.models import Movie
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


class Saved(models.Model):
    user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='telegram_saved_movie')

    def __str__(self):
        return self.movie.title
