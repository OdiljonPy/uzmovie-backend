from rest_framework import serializers
from .models import Movie, Director, Comment, Saved, Genre, Country, Language


class SearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = (
            'id', 'title', 'subscription_type', 'movie_rating', 'countries', 'description',
            'release_date', 'language', 'genres', 'actors', 'directors'
        )


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            'id', 'user', 'movie', 'content', 'rating',  # is active
        )


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ('id', 'name')


class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = ('id', 'name')


class SavedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Saved
        fields = ('user', 'movie')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('id', 'name')


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ('id', 'name')


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = (
            'id', 'title', 'movie_rating', 'description',
            'release_date', 'subscription_type', 'directors', 'genres', 'actors', 'countries', 'language'
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['directors'] = {
            "id": instance.directors.id,
            "name": instance.directors.name
        }
        data['countries'] = {
            "id": instance.countries.id,
            "name": instance.countries.name
        }
        data['language'] = {
            "id": instance.language.id,
            "name": instance.language.name
        }
        data['genres'] = [
            {"id": genre.id, "name": genre.name} for genre in instance.genres.all()
        ]
        data['actors'] = [
            {"id": actor.id, "name": actor.name} for actor in instance.actors.all()
        ]
        data['subscription_type'] = {
            "id": instance.subscription_type,
            "name": instance.get_subscription_type_display()
        }
        return data
