from django.contrib.auth.models import User
from django.http import Http404
from rest_framework import serializers
from .models import (
    Movie, Comment,
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


class MovieSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = '__all__'
        read_only_fields = ('author',)

    def save(self, **kwargs):
        request = self.context['request']
        user = User.objects.filter(user_id=request.user.id).first()

        if user is None:
            raise Http404('User not found')

        self.validated_data['author'] = user

        return super().save(**kwargs)
