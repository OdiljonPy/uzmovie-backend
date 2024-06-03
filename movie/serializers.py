from rest_framework import serializers
from .models import Movie, Director, Comment, Saved, Genre, Country


class SearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            'id', 'user', 'movie', 'content', 'rating', 'rated', 'created_at', 'updated_at'
        )


class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = '__all__'


class SavedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Saved
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'


class MovieSerializer(serializers.ModelSerializer):
    directors = serializers.SerializerMethodField()
    genres = serializers.SerializerMethodField()
    actors = serializers.SerializerMethodField()
    countries = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = [
            'id', 'title', 'subscription_type', 'imdb_rating', 'p_rating', 'description',
            'release_date', 'directors', 'genres', 'actors', 'countries'
        ]

    def get_directors(self, obj):
        director = obj.directors
        return {"id": director.id, "name": director.name}

    def get_countries(self, obj):
        country = obj.countries
        return {"id": country.id, "name": country.name}

    def get_genres(self, obj):
        genres = obj.genres.all()
        return [{"id": genre.id, "name": genre.name} for genre in genres]

    def get_actors(self, obj):
        actors = obj.actors.all()
        return [{"id": actor.id, "name": actor.name} for actor in actors]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['genres'] = self.get_genres(instance)
        representation['actors'] = self.get_actors(instance)
        return representation
