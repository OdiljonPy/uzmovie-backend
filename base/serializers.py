from rest_framework import serializers
from .models import Contact, About
from movie.models import Movie
from django.conf import settings


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ('id', 'first_name', 'last_name', 'email', 'phone_number', 'message')


class AboutSerializer(serializers.ModelSerializer):
    class Meta:
        model = About
        fields = ('id', 'phone_number', 'email', 'location', 'qr_image', 'movie_number', 'for_advertise')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get("request")
        lang = request.headers.get('Accept-Language', settings.MODELTRANSLATION_DEFAULT_LANGUAGE)

        lang_options = settings.MODELTRANSLATION_LANGUAGES

        if lang in lang_options:
            data['location'] = getattr(instance, f'location_{lang}')

        movies = Movie.objects.all()
        movie_length = len(movies)
        data['movie_number'] = movie_length
        return data
