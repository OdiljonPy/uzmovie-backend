from django.db.models import Q, Avg
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from .models import Movie, Saved, Comment
from rest_framework import status
from .serializers import MovieSerializer, CommentSerializer, SavedSerializer
from authentication.models import User
from .utils import check_premium
import math
from difflib import SequenceMatcher


class SearchViewSet(ViewSet):
    @swagger_auto_schema(
        operation_description="Search movie by name",
        operation_summary="Search movie by name",
        manual_parameters=[
            openapi.Parameter('page', type=openapi.TYPE_INTEGER, description='page', in_=openapi.IN_QUERY),
            openapi.Parameter('size', type=openapi.TYPE_INTEGER, description='size', in_=openapi.IN_QUERY),
            openapi.Parameter('search', type=openapi.TYPE_STRING, description='search', in_=openapi.IN_QUERY),
        ],
        responses={
            200: MovieSerializer(),
            404: 'Not found'
        },
        tags=['movie']
    )
    def search(self, request, *args, **kwargs):
        search = request.GET.get('search')
        page = int(request.GET.get('page', 1))
        size = int(request.GET.get('size', 10))
        movies = Movie.objects.all()

        if not str(page).isdigit() or int(page) < 1:
            return Response(data={'error': 'page must be greater than 0'}, status=status.HTTP_400_BAD_REQUEST)
        if not str(size).isdigit() or int(size) < 1:
            return Response(data={'error': 'size must be greater than 0'}, status=status.HTTP_400_BAD_REQUEST)

        if search is not None:
            movies = Movie.objects.filter(Q(title__icontains=search) | Q(description__icontains=search))
        total = movies.count()

        start = (page - 1) * size
        end = page * size
        serializer = MovieSerializer(movies[start:end], many=True)

        return Response(
            {
                'movies': serializer.data,
                'total': total,
                'page': page,
                'last_page': math.ceil(total / size)
            },
            status=status.HTTP_200_OK

        )


class MovieViewSet(ViewSet):
    @swagger_auto_schema(
        operation_description="Filter Movies",
        operation_summary="Filter Movies",
        manual_parameters=[
            openapi.Parameter('page', type=openapi.TYPE_INTEGER, description='page', in_=openapi.IN_BODY),
            openapi.Parameter('size', type=openapi.TYPE_INTEGER, description='size', in_=openapi.IN_BODY),
            openapi.Parameter('actor', type=openapi.TYPE_STRING, description='actor', in_=openapi.IN_BODY),
            openapi.Parameter('director', type=openapi.TYPE_STRING, description='director', in_=openapi.IN_BODY),
            openapi.Parameter('genre', type=openapi.TYPE_STRING, description='genre', in_=openapi.IN_BODY),
            openapi.Parameter('country', type=openapi.TYPE_STRING, description='country', in_=openapi.IN_BODY),
            openapi.Parameter('movie_rating', type=openapi.TYPE_INTEGER, description='movie_rating',
                              in_=openapi.IN_BODY),
            openapi.Parameter('release_date', type=openapi.TYPE_INTEGER, description='release_date',
                              in_=openapi.IN_BODY),
        ],
        responses={200: MovieSerializer()},
        tags=['movie']
    )
    def filter(self, request, *args, **kwargs):

        page = int(request.GET.get('page', 1))
        size = int(request.GET.get('size', 10))

        actor = request.data.get('actor')
        director = request.data.get('director')
        genre = request.data.get('genre')
        country = request.data.get('country')
        release_date = request.data.get('release_date')
        movie_rating = request.data.get('movie_rating')
        movies = Movie.objects.all().order_by('-release_date')

        similarity_threshold = 0.6

        def is_similar(value, query):
            return SequenceMatcher(None, value, query).ratio() >= similarity_threshold

        if actor:
            movies = [movie for movie in movies if
                      any(is_similar(actor, actor_name) for actor_name in movie.actors.values_list('name', flat=True))]
        if director:
            movies = [movie for movie in movies if any(is_similar(director, director_name) for director_name in
                                                       movie.directors.values_list('name', flat=True))]
        if genre:
            movies = [movie for movie in movies if
                      any(is_similar(genre, genre_name) for genre_name in movie.genres.values_list('name', flat=True))]
        if country:
            movies = [movie for movie in movies if is_similar(country, movie.country.name)]
        if release_date:
            movies = [movie for movie in movies if movie.release_date == release_date]
        if movie_rating:
            movies = [movie for movie in movies if is_similar(movie_rating, movie.movie_rating)]

        total = len(movies)
        start = (page - 1) * size
        end = page * size

        serializer = MovieSerializer(movies[start:end], many=True)
        return Response(
            {
                'movies': serializer.data,
                'total': total,
                'page': page,
                'last_page': math.ceil(total / size)
            },
            status=status.HTTP_200_OK
        )

    @swagger_auto_schema(
        operation_description="Get One Movie",
        operation_summary="Get One Movie",
        manual_parameters=[
            openapi.Parameter('get', type=openapi.TYPE_STRING, description='get by id', in_=openapi.IN_BODY)
        ],
        responses={200: MovieSerializer()},
        tags=['movie']
    )
    def get_by_id(self, request, *args, **kwargs):
        movie_id = kwargs.get('pk')
        response = check_premium(request.user, movie_id)
        return response


class CommentViewSet(ViewSet):
    # get_by_id
    @swagger_auto_schema(
        operation_description="Get Comment by id",
        operation_summary="Get Comment by id",
        manual_parameters=[
            openapi.Parameter(
                'id', type=openapi.TYPE_INTEGER, description='Comment id', in_=openapi.IN_BODY, required=True
            )
        ],
        responses={
            404: 'Not Found',
            200: CommentSerializer()
        },
        tags=['movie']
    )
    def get_by_id(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(data={'error': 'Not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)

        comment = Comment.objects.filter(id=kwargs['pk']).first()
        if comment is None:
            return Response(data={'error': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)

        return Response(data=CommentSerializer(comment).data, status=status.HTTP_200_OK)

    # create
    @swagger_auto_schema(
        operation_description="Create Comment",
        operation_summary="Create Comment",
        manual_parameters=[
            openapi.Parameter(
                'movie', type=openapi.TYPE_INTEGER, description='movie_id', in_=openapi.IN_BODY, required=True),
            openapi.Parameter(
                'content', type=openapi.TYPE_STRING, description='message', in_=openapi.IN_BODY, required=True),
            openapi.Parameter(
                'rating', type=openapi.TYPE_INTEGER, description='rating', in_=openapi.IN_BODY, required=True),
        ],
        responses={
            404: 'Not Found',
            200: CommentSerializer()
        },
        tags=['movie']
    )
    def comment_create(self, request, *args, **kwargs):
        movie = Movie.objects.filter(id=request.data['movie']).first()
        if movie is None:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={'message': 'Movie Not Found'}
            )
        user = request.user

        if not request.user.is_authenticated:
            return Response(data={'error': 'Not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)

        request.data['user'] = user.id
        serializer = CommentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.validated_data['user'] = user
            comment = Comment.objects.filter(user=user, movie=movie, rating__gt=0).first()
            rate_comment = Comment.objects.filter(movie=movie, rating__gt=0)

            if comment is None:
                serializer.save()
                average = rate_comment.aggregate(Avg('rating'))['rating__avg']
                average = round(average, 2)
                movie.movie_rating = average
                movie.save(update_fields=['movie_rating'])
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)

            serializer.validated_data['rating'] = 0
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # destroy
    @swagger_auto_schema(
        operation_description="Delete Comment bt id",
        operation_summary="Delete Comment bt id",
        manual_parameters=[
            openapi.Parameter(
                'id', type=openapi.TYPE_INTEGER, description='comment id', in_=openapi.IN_BODY, required=True)
        ],
        responses={
            404: 'Not Found',
            200: 'Successfully Deleted'
        },
        tags=['movie']
    )
    def comment_destroy(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(data={'error': 'Not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)

        comment = Comment.objects.filter(id=kwargs['pk']).first()

        if comment is None:
            return Response(data={'error': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)

        if comment.user != request.user:
            return Response(
                data={'error': 'You do not have permission to delete this comment'}, status=status.HTTP_400_BAD_REQUEST
            )
        comment.delete()

        movie = Movie.objects.filter(id=comment.movie.id).first()
        if movie is None:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={'message': 'Movie Not Found'}
            )
        rate_comment = Comment.objects.filter(movie=movie, rating__gt=0)
        average = rate_comment.aggregate(Avg('rating'))['rating__avg']

        if average is not None:
            movie.overall_rating = average
            movie.save(update_fields=['movie_rating'])

        movie.overall_rating = 0
        movie.save(update_fields=['movie_rating'])
        return Response(data={'message': 'Successfully deleted'}, status=status.HTTP_200_OK)


class SavedViewSet(ViewSet):

    @swagger_auto_schema(
        operation_description="Saved movie by id",
        operation_summary="Saved movie by id",
        manual_parameters=[
            openapi.Parameter('save', type=openapi.TYPE_INTEGER, description='save', in_=openapi.IN_BODY),
        ],
        responses={
            200: MovieSerializer(),
            404: 'Not found'
        },
        tags=['movie']
    )
    def save_movie(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(
                status=status.HTTP_401_UNAUTHORIZED,
                data={'detail': 'Not authenticated'},
            )
        user = User.objects.filter(id=request.user.id).first()
        movie = Movie.objects.filter(id=request.data['id']).first()
        if not movie:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={'detail': 'Movie not found'},
            )

        save = Saved.objects.filter(user=user, movie=movie).first()
        if save is None:
            save = Saved.objects.create(user_id=user.id, movie_id=request.data['id'])
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

    @swagger_auto_schema(
        operation_description="Saved movie list",
        operation_summary="Saved movie list",
        manual_parameters=[
            openapi.Parameter('saved', type=openapi.TYPE_INTEGER, description='saved', in_=openapi.IN_BODY),
        ],
        responses={
            200: MovieSerializer(),
            404: 'Not found'
        },
        tags=['movie']
    )
    def saved(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(
                status=status.HTTP_401_UNAUTHORIZED,
                data={'detail': 'Not authenticated'},
            )

        user = request.user
        # movies = Movie.objects.all()
        page = int(request.data.get('page', 1))
        size = int(request.data.get('size', 10))
        save = Saved.objects.filter(user=user)

        if not str(page).isdigit() or int(page) < 1:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': 'Page must be an positive integer'})
        if not str(size).isdigit() or int(size) < 1:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': 'Size must be an positive integer'})
        total = save.count()
        start = (page - 1) * size
        end = page * size
        serializer = SavedSerializer(save[start:end], many=True)

        return Response(
            {
                'movies': serializer.data,
                'total': total,
                'page': page,
                'last_page': math.ceil(total / size)
            },
            status=status.HTTP_200_OK

        )
