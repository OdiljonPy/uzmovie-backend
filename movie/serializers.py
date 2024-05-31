from django.contrib.auth.models import User
from django.http import Http404
from rest_framework import serializers
from .models import (
    Movie, Comment, Genre, Actor, Director,
)


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('author',)

    def save(self, **kwargs):
        request = self.context['request']
        user = User.objects.filter(user_id=request.user.id).first()

        if user is None:
            raise Http404('User not found')

        self.validated_data['author'] = user

        return super().save(**kwargs)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = '__all__'


class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = '__all__'


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        representation['comments'] = CommentSerializer(Comment.objects.filter(movie_id=instance.id), many=True).data
        representation['genres'] = GenreSerializer(instance.genre, many=True).data
        representation['actors'] = ActorSerializer(instance.actors, many=True).data
        representation['directors'] = DirectorSerializer(instance.directors, many=True).data
