from django.db import models

from movie.models import Movie


class TelegramUser(models.Model):
    user_id = models.IntegerField()
    balance = models.IntegerField(default=0)
    is_subscribed = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user_id)


class Saved(models.Model):
    user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='telegram_saved_movie')

    def __str__(self):
        return self.movie.title
