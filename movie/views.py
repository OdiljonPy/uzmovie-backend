from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from .models import Movie, Actor, Director, Genre, Saved
from rest_framework import status
from .serializers import MovieSerializer
from rest_framework.permissions import IsAuthenticated
from authentication.models import User


class MovieViewSet(ViewSet):
    serializer_class = MovieSerializer
    permission_classes = [IsAuthenticated]

    def get_all(self):
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)

    def get_by_id(self, pk=None):
        movie = Movie.objects.get(pk=pk)
        serializer = MovieSerializer(movie)
        return Response(serializer.data)

    def get_by_actor(self, request):
        actor_id = request.data.get('actor_id')
        if not actor_id:
            return Response({'error': 'Actor ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        movies = Movie.objects.filter(actor=actor_id)
        if movies.exists():
            return Response(self.serializer_class(movies, many=True).data)
        return Response({'error': 'Movie with this actor not found'}, status=status.HTTP_404_NOT_FOUND)

    def get_by_director(self, request):
        director_id = request.data.get('director_id')
        if not director_id:
            return Response({'error': 'Director ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        movies = Movie.objects.filter(director=director_id)
        if movies.exists():
            return Response(self.serializer_class(movies, many=True).data)
        return Response({'error': 'Movie with this director not found'}, status=status.HTTP_404_NOT_FOUND)

    def get_by_genre(self, request):
        genre_id = request.data.get('genre_id')
        if not genre_id:
            return Response({'error': 'Genre ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        movies = Movie.objects.filter(genres=genre_id)
        if movies.exists():
            return Response(self.serializer_class(movies, many=True).data)
        return Response({'error': 'Movie with this genre not found'}, status=status.HTTP_404_NOT_FOUND)


class SavedViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    def save_movie(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(
                status=status.HTTP_401_UNAUTHORIZED,
                data={'detail': 'Not authenticated'},
            )
        my_user = User.objects.filter(id=request.user.id).first()
        save = Saved.objects.filter(user_id=my_user.id, movie_id=kwargs['pk']).first()
        if save is None:
            save = Saved.objects.create(user_id=my_user.id, movie_id=kwargs['pk'])
            save.save()
            return Response(
                status=status.HTTP_201_CREATED,
                data={'message': 'Movie saved'}
            )
        save.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT,
            data={'message': 'Movie deleted'}
        )
