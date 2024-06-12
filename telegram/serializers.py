from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from movie.models import Movie
from movie.serializers import MovieSerializer
from .models import Saved


class SavedSerializer(ModelSerializer):
    class Meta:
        model = Saved
        fields = ('id', 'user', 'movie', 'created_at', 'updated_at')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['movie'] = MovieSerializer(Movie.objects.filter(id=data['movie']).first()).data
        return data['movie']


class MoviePaginationSerializer(serializers.Serializer):
    total = serializers.IntegerField()
    limit = serializers.IntegerField()
    current_page = serializers.IntegerField()
    has_next = serializers.BooleanField()
    has_previous = serializers.BooleanField()
    data = MovieSerializer(many=True)
