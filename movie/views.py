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

    def get_by_title(self, request):
        name = request.data.get('name', None)
        if name:
            try:
                movie = Movie.objects.get(name__iexact=name)
                serializer = self.serializer_class(movie)
                return Response(serializer.data)
            except Movie.DoesNotExist:
                return Response({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'Name parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

    def get_by_actor(self, request):
        actor_name = request.data.get('actor', None)
        if actor_name:
            try:
                actor = Actor.objects.get(name__iexact=actor_name)
                movies = Movie.objects.filter(actors=actor)
                if movies.exists():
                    serializer = self.serializer_class(movies, many=True)
                    return Response(serializer.data)
                else:
                    return Response({'error': 'Movies not found'}, status=status.HTTP_404_NOT_FOUND)
            except Actor.DoesNotExist:
                return Response({'error': 'Actor not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'Actor parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

    def get_by_director(self, request):
        director_name = request.data.get('director', None)
        if director_name:
            try:
                director = Director.objects.get(name__iexact=director_name)
                movies = Movie.objects.filter(directors=director)
                if movies.exists():
                    serializer = self.serializer_class(movies, many=True)
                    return Response(serializer.data)
                else:
                    return Response({'error': 'Movies not found'}, status=status.HTTP_404_NOT_FOUND)
            except Director.DoesNotExist:
                return Response({'error': 'Director not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'Director parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

    def get_by_genre(self, request):
        genre_name = request.data.get('genre', None)
        if genre_name:
            try:
                genre = Genre.objects.get(name__iexact=genre_name)
                movies = Movie.objects.filter(genres=genre)
                if movies.exists():
                    serializer = self.serializer_class(movies, many=True)
                    return Response(serializer.data)
                else:
                    return Response({'error': 'Movies not found'}, status=status.HTTP_404_NOT_FOUND)
            except Genre.DoesNotExist:
                return Response({'error': 'Genre not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'Genre parameter is required'}, status=status.HTTP_400_BAD_REQUEST)


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
