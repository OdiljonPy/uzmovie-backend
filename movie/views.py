from django.core.paginator import Paginator
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

        actor_id = request.GET.get('actor_id')

        if actor_id is not None:
            movies = Movie.objects.filter(actor_id=actor_id, is_published=True)

        director_id = request.GET.get('director_id')

        if director_id is not None:
            movies = Movie.objects.filter(director_id=director_id, is_published=True)

        genre_id = request.GET.get('genre_id')

        if genre_id is not None:
            movies = Movie.objects.filter(genre_id=genre_id, is_published=True)

        type_id = request.GET.get('type_id')

        if type_id is not None:
            movies = Movie.objects.filter(type_id=type_id, is_published=True)

        premium_id = request.GET.get('premium_id')

        if premium_id is not None:
            movies = Movie.objects.filter(premium=True, is_published=True)

        serializer = MovieSerializer(movies, many=True)

        return Response({'movies': serializer.data}, status=status.HTTP_200_OK)

    def retrieve_movie(self, request, *args, **kwargs):
        pk = kwargs.get('pk')

        if pk is None:
            return Response({'message': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)

        movie = Movie.objects.filter(pk=pk, is_published=True).first()

        if movie is None:
            return Response({'message': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = MovieSerializer(movie)

        return Response({'message': serializer.data}, status=status.HTTP_200_OK)


class CommentListCreateViewSet(ViewSet):
    permission_classes = (IsAuthenticated,)

    def list_comments(self, request, *args, **kwargs):
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)

        return Response({'comments': serializer.data}, status=status.HTTP_200_OK)

    def create_comment(self, request, *args, **kwargs):
        serializer = CommentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response({'message': 'Product created'}, status=status.HTTP_201_CREATED)

        return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class UtilsViewSet(ViewSet):
    permission_classes = (IsAuthenticated,)

    def pagination(self, request, *args, **kwargs):
        page = request.data.get('page', 1)
        size = request.data.get('size', 5)

        page = int(page)
        size = int(size)

        if page < 1 or size < 1:
            return Response({'error': 'Page and size must be positive integers.'}, status=status.HTTP_400_BAD_REQUEST)

        movies = Movie.objects.filter(is_published=True)

        paginator = Paginator(movies, size)
        result = paginator.page(page)
        serializer = MovieSerializer(result, many=True)

        return Response({'movies': serializer.data}, status=status.HTTP_201_CREATED)

    def search(self, request, *args, **kwargs):
        query = request.data.get('q')

        if query is None:
            return Response({'message': 'Query is required'}, status=status.HTTP_404_NOT_FOUND)

        movies = Movie.objects.filter(title__contains=query, is_published=True)
        serializer = MovieSerializer(movies, many=True)

        return Response({'movies': serializer.data}, status=status.HTTP_200_OK)

    def rating(self, request, *args, **kwargs):
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
            return Response({'message': 'Already added'}, status=status.HTTP_404_NOT_FOUND)

        new_movie_rating = MovieRating.objects.create(movie_id=movie_id, user_id=user_id, rating=rating)
        new_movie_rating.save()

        movie = Movie.objects.filter(movie_id=movie_id).first()
        movie.imdb_rating += new_movie_rating.rating
        movie.save(update_fields=['imdb_rating'])

        return Response({'message': 'Movie rating successfully added'}, status=status.HTTP_201_CREATED)

    def saved(self, request, *args, **kwargs):
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
            item = Saved.objects.create(user_id=user_id, movie_id=movie_id)
            item.save()

            return Response({'message': 'Saved successfully'}, status=status.HTTP_201_CREATED)

        saved_item.delete()

        return Response({'message': 'Saved item successfully deleted'}, status=status.HTTP_204_NO_CONTENT)

    def list_saved(self, request, *args, **kwargs):
        user_id = request.user.id

        if user_id is None:
            return Response({'message': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)

        saved_movies = Saved.objects.filter(user_id=user_id)
        movies = [Movie.objects.filter(movie_id=i.movie_id) for i in saved_movies]
        serializer = MovieSerializer(movies, many=True)

        return Response({'movies': serializer.data}, status=status.HTTP_200_OK)
