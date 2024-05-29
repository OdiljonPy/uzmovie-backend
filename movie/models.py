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
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)

    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    genre = models.ManyToManyField(Genre)
    actors = models.ManyToManyField(Actor)
    directors = models.ForeignKey(Director, on_delete=models.CASCADE)

    description = models.TextField()
    release_date = models.DateField()
    imdb_rating = models.FloatField()

    is_published = models.BooleanField(default=True)

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
    rating = models.FloatField()  # Could not get it

    is_active = models.BooleanField(default=True)

    # TODO: datetime migrate error


class MovieRating(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating = models.FloatField()

    def __str__(self):
        return self.movie.title
