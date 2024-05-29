from django.contrib.auth.models import User
from django.db import models


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


class Movie(models.Model):
    title = models.CharField(max_length=200)
    type = models.ForeignKey(Type, on_delete=models.CASCADE, blank=True, null=True)  # cartoons, serials, more action
    imdb_rating = models.FloatField()
    description = models.TextField()
    release_date = models.DateField()
    genre = models.ManyToManyField(Genre)
    actors = models.ManyToManyField(Actor)
    directors = models.ForeignKey(Director, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Saved(models.Model):
    # user = models.ForeignKey(MyUser, on_delete=models.CASCADE)  # write after authentication
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    saved_at = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    # user = models.ForeignKey(MyUser, on_delete=models.CASCADE) # write after authentication
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    content = models.TextField()  # message
    rating = models.FloatField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)
