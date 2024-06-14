from django.db import models
from authentication.models import User

MOVIE_SUBSCRIPTION_TYPE = (
    (1, "FREE"),
    (2, "PREMIUM")
)
LANGUAGE_CHOICES = (
    (1, "English"),
    (2, "Russian"),
    (3, "Uzbek")
)


class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Actor(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="actors/")
    url = models.URLField(max_length=500)

    def __str__(self):
        return self.name


class Director(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="directors/")
    url = models.URLField(max_length=500)

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=200)
    subscription_type = models.IntegerField(choices=MOVIE_SUBSCRIPTION_TYPE)
    movie_rating = models.FloatField(default=0)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    description = models.TextField()
    release_date = models.PositiveIntegerField(default=0)
    language = models.IntegerField(choices=LANGUAGE_CHOICES)
    genres = models.ManyToManyField(Genre)
    actors = models.ManyToManyField(Actor)
    directors = models.ManyToManyField(Director)
    premiere_date = models.DateField(blank=True, null=True)

    video = models.FileField(upload_to='movie_videos/')
    image = models.ImageField(upload_to='movie_images/')

    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.title


class Saved(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.movie


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    content = models.TextField()
    rating = models.FloatField(default=0)

    is_visible = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.user
