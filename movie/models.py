from django.db import models
from authentication.models import User

MOVIE_SUBSCRIPTION_TYPE = (
    (1, "FREE"),
    (2, "PREMIUM")
)


class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Language(models.Model):
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
    subscription_type = models.IntegerField(choices=MOVIE_SUBSCRIPTION_TYPE)
    imdb_rating = models.FloatField()
    p_rating = models.FloatField(default=0)
    countries = models.ForeignKey(Country, on_delete=models.CASCADE)
    description = models.TextField()
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    release_date = models.DateField()
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    genres = models.ManyToManyField(Genre)
    actors = models.ManyToManyField(Actor)
    directors = models.ForeignKey(Director, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Saved(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    saved_at = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    content = models.TextField()  # message
    rating = models.FloatField()
    rated = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)
