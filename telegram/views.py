from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status

from movie.models import Movie
from movie.serializers import MovieSerializer
from .models import TelegramUser, Saved
from .serializers import SavedSerializer


class MovieViewSet(ViewSet):
    @swagger_auto_schema(
        operation_description="Filter Movies From Telegram",
        operation_summary="Filter Movies From Telegram",
        manual_parameters=[
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
        if data.get("title"):
            movies = Movie.objects.filter(title__contains=data['title'])
        elif data.get("actor"):
            movies = Movie.objects.filter(actors__name__contains=data['actor'])
        elif data.get("director"):
            movies = Movie.objects.filter(directors__name__contains=data['director'])
        elif data.get("genre"):
            movies = Movie.objects.filter(genre__name=data['genre'].upper())
        else:
            movies = Movie.objects.all()

        serializer = MovieSerializer(movies, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Get One Movie From Telegram",
        operation_summary="Get One Movie From Telegram",
        responses={200: MovieSerializer()},
        tags=['Telegram']
    )
    def get_by_id(self, request, *args, **kwargs):
        movie = Movie.objects.filter(id=kwargs['pk']).first()
        user = TelegramUser.objects.filter(username=request.GET.get('username')).first()
        if movie.is_premium and not user.is_subscribed:
            return Response(data={'error': 'This movie is only for premium users'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = MovieSerializer(movie)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class SavedViewSet(ViewSet):
    @swagger_auto_schema(
        operation_description="Get Movies From Saved",
        operation_summary="Get Movies From Saved",
        manual_parameters=[
            openapi.Parameter('username', type=openapi.TYPE_STRING, description='username', in_=openapi.IN_QUERY,
                              required=True),
        ],
        responses={200: SavedSerializer()},
        tags=['Telegram']
    )
    def get(self, request, *args, **kwargs):
        movies = Saved.objects.filter(user__username=request.GET.get('username'))
        serializer = SavedSerializer(movies, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Add to Saved",
        operation_summary="Add to Saved",
        manual_parameters=[
            openapi.Parameter('username', type=openapi.TYPE_STRING, description='username', in_=openapi.IN_QUERY,
                              required=True),
            openapi.Parameter('movie', type=openapi.TYPE_INTEGER, description='movie_id', in_=openapi.IN_QUERY,
                              required=True),
        ],
        responses={201: SavedSerializer()},
        tags=['Telegram']
    )
    def post(self, request, *args, **kwargs):
        data = request.data
        movie = Saved.objects.filter(user__username=data['username'], movie_id=data['movie']).first()
        if movie:
            return Response(data={"message": "This movie was already added"}, status=status.HTTP_200_OK)
        data['user'] = TelegramUser.objects.filter(username=data['username']).first().id
        serializer = SavedSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Delete Movie From Saved",
        operation_summary="Delete Movie From Saved",
        manual_parameters=[
            openapi.Parameter('username', type=openapi.TYPE_STRING, description='username', in_=openapi.IN_QUERY,
                              required=True),
            openapi.Parameter('movie', type=openapi.TYPE_INTEGER, description='movie', in_=openapi.IN_QUERY,
                              required=True),
        ],
        responses={200: "Successfully deleted"},
        tags=['Telegram']
    )
    def delete(self, request, *args, **kwargs):
        data = request.data
        movie = Saved.objects.filter(user__username=data.get('username'), movie_id=data.get('movie')).first()
        if movie:
            movie.delete()
            return Response(data={"message": "Successfully deleted"}, status=status.HTTP_200_OK)
        return Response(data={"error": "Movie not found"}, status=status.HTTP_400_BAD_REQUEST)
