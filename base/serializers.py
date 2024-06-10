from rest_framework import serializers
from .models import Contact, About


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ('id', 'first_name', 'last_name', 'email', 'phone_number', 'message')


class AboutSerializer(serializers.ModelSerializer):
    class Meta:
        model = About
        fields = ('id', 'phone_number', 'email', 'watch_movie', 'location', 'qr_image', 'movie_number', 'for_advertise')
