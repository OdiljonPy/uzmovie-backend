from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from authentication.models import User
from .serializers import (
    MovieSerializer, CommentSerializer,
)
from .models import (
    Movie, Saved, Comment, MovieRating,
)


class MovieListCreateViewSet(ViewSet):
    permission_classes = (IsAuthenticated,)

    def list_movies(self, request, *args, **kwargs):
        movies = Movie.objects.filter(is_published=True)

        if movies is None:
            return Response({'message': 'No movies found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = MovieSerializer(movies, many=True)

        return Response({'movies': serializer.data}, status=status.HTTP_200_OK)

    def retrieve_movie(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        movie = Movie.objects.filter(pk=pk, is_published=True).first()

        if movie is None:
            return Response({'message': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)

        comments = Comment.objects.filter(movie_id=pk)

        if comments is None:
            return Response({'message': 'No comments found'}, status=status.HTTP_400_BAD_REQUEST)

        movie.comments = comments
        serializer = MovieSerializer(movie)

        return Response({'message': serializer.data}, status=status.HTTP_200_OK)

    def list_by_actor(self, request, *args, **kwargs):
        actor_id = kwargs.get('actor_id')

        if actor_id is None:
            return Response({'message': 'Actor ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        movies = Movie.objects.filter(actor=actor_id, is_published=True)

        if movies is None:
            return Response({'message': 'Movie not found'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = MovieSerializer(movies, many=True)

        return Response({'message': serializer.data}, status=status.HTTP_200_OK)

    def list_by_director(self, request, *args, **kwargs):
        director_id = kwargs.get('director_id')

        if director_id is None:
            return Response({'message': 'Director ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        movies = Movie.objects.filter(director=director_id, is_published=True)

        if movies is None:
            return Response({'message': 'Movie not found'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = MovieSerializer(movies, many=True)

        return Response({'message': serializer.data}, status=status.HTTP_200_OK)

    def list_by_genre(self, request, *args, **kwargs):
        genre_id = kwargs.get('genre_id')

        if genre_id is None:
            return Response({'message': 'Genre ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        movies = Movie.objects.filter(genres=genre_id, is_published=True)

        if movies is None:
            return Response({'message': 'Movies not found'}, status=status.HTTP_200_OK)

        serializer = MovieSerializer(movies, many=True)

        return Response({'message': serializer.data}, status=status.HTTP_200_OK)


class CommentListCreateViewSet(ViewSet):
    def create_comment(self, request, *args, **kwargs):
        serializer = CommentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response({'message': 'Product created'}, status=status.HTTP_201_CREATED)

        return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def list_comments(self, request, *args, **kwargs):
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)

        return Response({'comments': serializer.data}, status=status.HTTP_200_OK)


class SavedItemCreateDestroyViewSet(ViewSet):
    permission_classes = (IsAuthenticated,)

    def create_saved_item(self, request, *args, **kwargs):
        user_id = request.user.id

        if user_id is None:
            return Response({'message': 'User ID is required'}, status=status.HTTP_404_NOT_FOUND)

        user = User.objects.filter(id=request.user.id).first()

        if user is None:
            return Response({'message': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)

        movie_id = kwargs.get('movie_id')

        if movie_id is None:
            return Response({'message': 'Movie ID is required'}, status=status.HTTP_404_NOT_FOUND)

        movie = Movie.objects.filter(id=movie_id, is_published=True).first()

        if movie is None:
            return Response({'message': 'Movie does not exist'}, status=status.HTTP_404_NOT_FOUND)

        saved_item = Saved.objects.filter(user_id=user_id, movie_id=movie_id).first()

        if saved_item is not None:
            return Response({'message': 'Movie already exists'}, status=status.HTTP_409_CONFLICT)

        item = Saved.objects.create(user_id=user_id, movie_id=movie_id)
        item.save()

        return Response({'message': 'Saved successfully'}, status=status.HTTP_201_CREATED)

    def destroy_saved_item(self, request, *args, **kwargs):
        user_id = request.user.id

        if user_id is None:
            return Response({'message': 'User ID is required'}, status=status.HTTP_404_NOT_FOUND)

        user = User.objects.filter(id=request.user.id).first()

        if user is None:
            return Response({'message': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)

        movie_id = kwargs.get('movie_id')

        if movie_id is None:
            return Response({'message': 'Movie ID is required'}, status=status.HTTP_404_NOT_FOUND)

        movie = Movie.objects.filter(id=movie_id, is_published=True).first()

        if movie is None:
            return Response({'message': 'Movie does not exist'}, status=status.HTTP_404_NOT_FOUND)

        saved_item = Saved.objects.filter(user_id=user_id, movie_id=movie_id).first()

        if saved_item is None:
            return Response({'message': 'Movie does not exist'}, status=status.HTTP_204_NO_CONTENT)

        saved_item.delete()

        return Response({'message': 'Saved item successfully deleted'}, status=status.HTTP_204_NO_CONTENT)


class MovieRatingViewSet(ViewSet):
    permission_classes = ('IsAuthenticated',)

    def plus_minus_rating(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')

        if user_id is None:
            return Response({'message': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)

        movie_id = kwargs.get('movie_id')

        if movie_id is None:
            return Response({'message': 'Movie ID is required'}, status=status.HTTP_404_NOT_FOUND)

        rating = request.data.get('rating')

        if rating is None:
            return Response({'message': 'Rating is required'}, status=status.HTTP_404_NOT_FOUND)

        movie_rating = MovieRating.objects.filter(movie_id=movie_id, user_id=user_id).first()

        if movie_rating is not None:
            movie_rating.rating = rating
            movie_rating.save(update_fields=['rating'])

            return Response({'message': 'Movie rating deleted'}, status=status.HTTP_204_NO_CONTENT)

        new_movie_rating = MovieRating.objects.create(movie_id=movie_id, user_id=user_id, rating=rating)
        new_movie_rating.save()

        return Response({'message': 'Movie rating successfully added'}, status=status.HTTP_201_CREATED)
