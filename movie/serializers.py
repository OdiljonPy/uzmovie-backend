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

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['user'] = {
            "id": instance.user.id,
            "username": instance.user.username,
        }
        data['movie'] = {
            "id": instance.movie.id,
            "title": instance.movie.title,
        }
        return data


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
            'release_date', 'subscription_type', 'directors', 'genres', 'actors', 'country', 'language'
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['country'] = {"id": instance.country.id, "name": instance.country.name}
        data['language'] = {"id": instance.language.id, "name": instance.language.name}
        data['subscription_type'] = {"id": instance.subscription_type, "name": instance.get_subscription_type_display()}
        data['genres'] = list(map(lambda genre: {"id": genre.id, "name": genre.name}, instance.genres.all()))
        data['actors'] = list(map(lambda actor: {"id": actor.id, "name": actor.name}, instance.actors.all()))
        data['directors'] = list(
            map(lambda director: {"id": director.id, "name": director.name}, instance.directors.all()))
        return data
