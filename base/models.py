from django.db import models
from .validators import validate_uz_phone_number


class About(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    image = models.ImageField(upload_to='images/')
    phone_number = models.CharField(max_length=13, validators=[validate_uz_phone_number])
    email = models.EmailField()

    def __str__(self):
        return self.title


class Contact(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone_number = models.CharField(max_length=13, validators=[validate_uz_phone_number])
    message = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name}::{self.phone_number}"
