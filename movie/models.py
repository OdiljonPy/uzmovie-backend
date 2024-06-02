from django.contrib.auth.models import User
from django.db import models

MOVIE_SUBSCRIPTION_TYPE = (
    (1, "FREE"),
    (2, "PREMIUM")
)


class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Actor(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Director(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=200)
    subscription_type = models.IntegerField(choices=MOVIE_SUBSCRIPTION_TYPE, default=1)
    imdb_rating = models.FloatField()
    p_rating = models.FloatField(default=0)
    description = models.TextField()
    release_date = models.DateField()
    genre = models.ManyToManyField(Genre)
    actors = models.ManyToManyField(Actor)
    directors = models.ForeignKey(Director, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Saved(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # write after authentication

    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    saved_at = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # write after authentication
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    content = models.TextField()  # message
    rating = models.FloatField()
    rated = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)
