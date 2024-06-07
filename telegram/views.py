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
        page = data.get('page', 1)
        size = data.get('size', 2)

        if not str(page).isdigit() or int(page) < 1:
            return Response(data={'error': 'page must be greater than 0'}, status=status.HTTP_400_BAD_REQUEST)
        if not str(size).isdigit() or int(size) < 1:
            return Response(data={'error': 'size must be greater than 0'}, status=status.HTTP_400_BAD_REQUEST)

        query = "SELECT * FROM movie_movie m "
        condition = "WHERE "
        if data.get("actor"):
            query += "JOIN movie_movie_actors ma ON m.id = ma.movie_id JOIN movie_actor a ON ma.actor_id = a.id "
            condition += f"a.name LIKE '%{data['actor']}%' and "
        if data.get("director"):
            query += "JOIN movie_director d ON m.directors_id = d.id "
            condition += f"d.name LIKE '%{data['director']}%' and "
        if data.get("genre"):
            query += f"JOIN movie_movie_genre mg ON m.id = mg.movie_id JOIN movie_genre g ON mg.genre_id = g.id "
            condition += f"g.name = '{data['genre'].capitalize()}' and "
        if data.get("title"):
            condition += f"m.title LIKE '%{data['title'].capitalize()}%' and "

        paginator = Paginator(Movie, size, page, query)
        if condition.find('and') != -1:
            paginator = Paginator(Movie, size, page, query + condition[:len(condition) - 4])
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
            return Response(data={'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
        if not user:
            return Response(data={'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
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
            return Response(data={'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
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
            return Response(data={'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        movie = Saved.objects.filter(user__user_id=data['user_id'], movie_id=data['movie']).first()
        if movie:
            movie.delete()
            return Response(data={"message": "Successfully deleted"}, status=status.HTTP_204_NO_CONTENT)
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
