from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from movie.models import Movie
from movie.serializers import MovieSerializer


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
            movies = Movie.objects.filter(title__contains=data['name'])
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
        if movie.is_premium and not request.user.is_subscribed:
            return Response(data={'error': 'This movie is only for premium users'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = MovieSerializer(movie)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
