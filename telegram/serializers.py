from rest_framework.serializers import ModelSerializer

from movie.models import Movie
from movie.serializers import MovieSerializer
from .models import Saved, TelegramUser


class SavedSerializer(ModelSerializer):
    class Meta:
        model = Saved
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['user'] = TelegramUser.objects.filter(id=data['user']).first().username
        data['movie'] = MovieSerializer(Movie.objects.filter(id=data['movie']), many=True).data
        return data