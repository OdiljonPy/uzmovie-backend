from django.db import models
from config.base_models import BaseModel
from authentication.models import User


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


class Type(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Movie(BaseModel):
    title = models.CharField(max_length=200)

    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    genres = models.ManyToManyField(Genre)
    actors = models.ManyToManyField(Actor)
    directors = models.ManyToManyField(Director)

    description = models.TextField()
    price = models.FloatField(default=0, blank=True, null=True)
    release_date = models.DateField()
    imdb_rating = models.FloatField(default=0)

    is_published = models.BooleanField(default=True)
    is_premium = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Saved(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # write after authentication
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    saved_at = models.DateTimeField(auto_now_add=True)


class Comment(BaseModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    content = models.TextField()

    is_active = models.BooleanField(default=True)


class MovieRating(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating = models.FloatField()

    def __str__(self):
        return self.movie.title
