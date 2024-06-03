from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from movie.models import Movie
from movie.serializers import MovieSerializer
from .core import Paginator
from .models import TelegramUser, Saved
from .serializers import SavedSerializer


class MovieViewSet(ViewSet):
    @swagger_auto_schema(
        operation_description="Filter Movies From Telegram",
        operation_summary="Filter Movies From Telegram",
        manual_parameters=[
            openapi.Parameter('page', type=openapi.TYPE_INTEGER, description='page', in_=openapi.IN_QUERY),
            openapi.Parameter('size', type=openapi.TYPE_INTEGER, description='size', in_=openapi.IN_QUERY),
            openapi.Parameter('title', type=openapi.TYPE_STRING, description='title', in_=openapi.IN_QUERY),
            openapi.Parameter('actor', type=openapi.TYPE_STRING, description='actor', in_=openapi.IN_QUERY),
            openapi.Parameter('director', type=openapi.TYPE_STRING, description='director', in_=openapi.IN_QUERY),
            openapi.Parameter('genre', type=openapi.TYPE_STRING, description='genre', in_=openapi.IN_QUERY),
        ],
        responses={200: MovieSerializer()},
        tags=['Telegram']
    )
    def filter(self, request, *args, **kwargs):
        data = request.GET
        page = 1
        if data.get('page'):
            page = int(data['page'])
        size = 2
        if data.get('size'):
            size = int(data['size'])
        if data.get("title"):
            query = f"SELECT * FROM movie_movie WHERE title LIKE '%{data['title']}%'"
            paginator = Paginator(Movie, size, page, query)
            movies = paginator.page()
        elif data.get("actor"):
            query = f"SELECT * FROM movie_movie m JOIN movie_movie_actors ma ON m.id = ma.movie_id JOIN movie_actor a ON (ma.actor_id = a.id) WHERE a.name LIKE '%{data['actor']}%'"
            paginator = Paginator(Movie, size, page, query)
            movies = paginator.page()
        elif data.get("director"):
            query = f"SELECT * FROM movie_movie m JOIN movie_director d ON m.directors_id = d.id WHERE d.name LIKE '%{data['director']}%'"
            paginator = Paginator(Movie, size, page, query)
            movies = paginator.page()
        elif data.get("genre"):
            query = f"SELECT * FROM movie_movie m JOIN movie_movie_genre mg ON m.id = mg.movie_id JOIN movie_genre g ON mg.genre_id = g.id WHERE g.name = '{data['genre'].capitalize()}'"
            paginator = Paginator(Movie, size, page, query)
            movies = paginator.page()
        else:
            query = "SELECT * FROM movie_movie"
            paginator = Paginator(Movie, size, page, query)
            movies = paginator.page()

        serializer = MovieSerializer(movies, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Get One Movie From Telegram",
        operation_summary="Get One Movie From Telegram",
        manual_parameters=[
            openapi.Parameter('user_id', type=openapi.TYPE_INTEGER, description='telegram user id',
                              in_=openapi.IN_QUERY, required=True),
        ],
        responses={200: MovieSerializer()},
        tags=['Telegram']
    )
    def get_by_id(self, request, *args, **kwargs):
        movie = Movie.objects.filter(id=kwargs['pk']).first()
        user = TelegramUser.objects.filter(user_id=request.GET.get('user_id')).first()
        if not movie:
            return Response(data={'error': 'Movie not found'}, status=status.HTTP_400_BAD_REQUEST)
        if not user:
            return Response(data={'error': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)
        if movie.subscription_type == 2 and not user.is_subscribed:
            return Response(data={'error': 'This movie is only for premium users'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = MovieSerializer(movie)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class SavedViewSet(ViewSet):
    @swagger_auto_schema(
        operation_description="Get Movies From Saved",
        operation_summary="Get Movies From Saved",
        manual_parameters=[
            openapi.Parameter('user_id', type=openapi.TYPE_INTEGER, description='telegram user id',
                              in_=openapi.IN_QUERY,
                              required=True),
        ],
        responses={200: SavedSerializer()},
        tags=['Telegram']
    )
    def get(self, request, *args, **kwargs):
        user = TelegramUser.objects.filter(user_id=request.GET.get('user_id')).first()
        if not user:
            return Response(data={'error': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)
        movies = Saved.objects.filter(user__user_id=user.user_id)
        serializer = SavedSerializer(movies, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Add to Saved",
        operation_summary="Add to Saved",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['user_id', 'movie'],
            properties={
                'user_id': openapi.Schema(type=openapi.TYPE_INTEGER, title='Telegram user id'),
                'movie': openapi.Schema(type=openapi.TYPE_INTEGER, title='Movie ID')
            }
        ),
        responses={201: SavedSerializer()},
        tags=['Telegram']
    )
    def post(self, request, *args, **kwargs):
        data = request.data
        user = TelegramUser.objects.filter(user_id=data.get('user_id')).first()
        if not user:
            return Response(data={'error': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)
        movie = Saved.objects.filter(user__user_id=data['user_id'], movie_id=data['movie']).first()
        if movie:
            movie.delete()
            return Response(data={"message": "Successfully deleted"}, status=status.HTTP_200_OK)
        data['user'] = TelegramUser.objects.filter(user_id=data['user_id']).first().id
        serializer = SavedSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AuthViewSet(ViewSet):
    @swagger_auto_schema(
        operation_description="Register",
        operation_summary="Register new user",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['user_id'],
            properties={'user_id': openapi.Schema(type=openapi.TYPE_INTEGER, title='Telegram user id')}
        ),
        responses={201: 'Successfully Registered'},
        tags=['Telegram']
    )
    def register(self, request, *args, **kwargs):
        user = TelegramUser.objects.filter(user_id=request.data.get('user_id')).first()
        if user:
            return Response(data={'message': 'This user was already registered'}, status=status.HTTP_200_OK)
        user = TelegramUser.objects.create(user_id=request.data.get('user_id'))
        user.save()
        return Response(data={'message': 'Successfully registered'}, status=status.HTTP_201_CREATED)
