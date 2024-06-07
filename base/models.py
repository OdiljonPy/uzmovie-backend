from django.db import models
from .utils import phone_number_validation

Status = (
    (1, 'sent to check'),
    (2, 'in progress'),
    (3, 'checked')

)


class About(models.Model):
    for_advertise = models.CharField(max_length=50)
    watch_movie = models.PositiveIntegerField()
    movie_number = models.PositiveIntegerField()
    qr_image = models.ImageField(upload_to='images/')
    location = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=13, validators=[phone_number_validation])
    email = models.EmailField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email


class Contact(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone_number = models.CharField(max_length=13, validators=[phone_number_validation])
    message = models.TextField()
    status = models.IntegerField(choices=Status, default=1)

    is_solved = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name}::{self.phone_number}"
