from django.contrib.auth.models import User
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from .serializers import MovieSerializer, CommentSerializer, SavedSerializer
from .models import Movie, Comment, Saved


class MovieViewSet(ViewSet):
    serializer_class = MovieSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Filter Movies",
        operation_summary="Filter Movies",
        manual_parameters=[
            openapi.Parameter('title', type=openapi.TYPE_STRING, description='title', in_=openapi.IN_QUERY),
            openapi.Parameter('actor', type=openapi.TYPE_STRING, description='actor', in_=openapi.IN_QUERY),
            openapi.Parameter('director', type=openapi.TYPE_STRING, description='director', in_=openapi.IN_QUERY),
            openapi.Parameter('genre', type=openapi.TYPE_STRING, description='genre', in_=openapi.IN_QUERY),
        ],
        responses={200: MovieSerializer()},
        tags=['movie']
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
            movies = Movie.objects.filter(genre__name__contains=data['genre'])
        else:
            movies = Movie.objects.all()

        serializer = MovieSerializer(movies, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Get One Movie",
        operation_summary="Get One Movie",
        responses={200: MovieSerializer()},
        tags=['movie']
    )
    def get_by_id(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(data={'error': 'Not authenticated'}, status=status.HTTP_404_NOT_FOUND)

        movie = Movie.objects.filter(id=kwargs['pk']).first()

        if movie is None:
            return Response(data={'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)

        comment = Comment.objects.filter(movie_id=movie)
        serializer = CommentSerializer(comment, many=True)
        return Response(data={
            'movie': MovieSerializer(movie).data,
            'comments': serializer.data
        }, status=status.HTTP_200_OK)


class SearchViewSet(ViewSet):
    @swagger_auto_schema(
        operation_description="Search movie by name",
        operation_summary="Search movie by name",
        manual_parameters=[
            openapi.Parameter('search', type=openapi.TYPE_STRING, description='search', in_=openapi.IN_QUERY),
        ],
        responses={200: MovieSerializer()},
        tags=['movie']
    )
    def search(self, request, *args, **kwargs):
        data = request.GET
        search = data.get('search')
        movies = Movie.objects.filter(name__icontains=search)  # faqat (name)i bo`yicha search
        serializer = MovieSerializer(movies, many=True)
        if movies is None:
            return Response(data={'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

        return Response(data={'movies': serializer.data}, status=status.HTTP_200_OK)


class CommentViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    # list
    @swagger_auto_schema(
        operation_description="List of all Comments",
        operation_summary="List of all Comments",
        responses={200: CommentSerializer()},
        tags=['movie']
    )
    def comment_list(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(data={'error': 'Not authenticated'}, status=status.HTTP_404_NOT_FOUND)

        return Response(data={'comments': CommentSerializer().data}, status=status.HTTP_200_OK)

    # review
    @swagger_auto_schema(
        operation_description="Review Comment by id",
        operation_summary="Review Comment by id",
        manual_parameters=[
            openapi.Parameter('id', type=openapi.TYPE_INTEGER, description='Comment id',
                              in_=openapi.IN_QUERY, required=True)
        ],
        responses={404: 'Not Found',
                   200: CommentSerializer()},
        tags=['movie']
    )
    def comment_review(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(data={'error': 'Not authenticated'}, status=status.HTTP_404_NOT_FOUND)

        comment = Comment.objects.filter(id=kwargs['pk']).first()
        if comment is None:
            return Response(data={'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

        return Response(data={'comment': CommentSerializer(comment).data}, status=status.HTTP_200_OK)

    # create
    @swagger_auto_schema(
        operation_description="Create Comment",
        operation_summary="Create Comment",
        manual_parameters=[
            openapi.Parameter(
                'movie id', type=openapi.TYPE_INTEGER, description='movie id', in_=openapi.IN_QUERY, required=True),
            openapi.Parameter(
                'message', type=openapi.TYPE_STRING, description='message', in_=openapi.IN_QUERY, required=True),
            openapi.Parameter(
                'rating', type=openapi.TYPE_INTEGER, description='rating', in_=openapi.IN_QUERY, required=True),
        ],
        responses={
            404: 'Not Found',
            200: CommentSerializer()
        },
        tags=['movie']
    )
    def comment_create(self, request, *args, **kwargs):
        r_movie = Movie.objects.filter(id=request.data['movie']).first()
        myuser_id = request.user
        if not request.user.is_authenticated:
            return Response(data={'error': 'Not authenticated'}, status=status.HTTP_404_NOT_FOUND)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['user'] = myuser_id
            check = Comment.objects.filter(user=myuser_id, movie=request.data['movie']).first()
            s = 0
            if check is None:
                serializer.save()
                comments = Comment.objects.filter(movie=request.data['movie']).all()
                comments_len = len(comments)
                for comment in comments:
                    s += comment.rating

                r_movie.imdb_rating = s / comments_len
                r_movie.save(update_fields=['imdb_rating'])
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
            return Response(data={'error': 'You`ve already commented this movie'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # destroy
    @swagger_auto_schema(
        operation_description="Delete Comment bt id",
        operation_summary="Delete Comment bt id",
        manual_parameters=[
            openapi.Parameter(
                'id', type=openapi.TYPE_INTEGER, description='comment id', in_=openapi.IN_QUERY, required=True)
        ],
        responses={
            404: 'Not Found',
            200: 'Successfully Deleted'
        },
        tags=['movie']

    )
    def comment_destroy(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(data={'error': 'Not authenticated'}, status=status.HTTP_404_NOT_FOUND)

        comment = Comment.objects.filter(id=kwargs['pk']).first()
        if comment is None:
            return Response(data={'error': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)

        comment.delete()
        return Response(data={'message': 'Successfully deleted'}, status=status.HTTP_200_OK)


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

    def list_movie(self, request, *args, **kwargs):
        user = request.user
        save = Saved.objects.filter(user=user)
        serializer = SavedSerializer(save, many=True)
        return Response(
            data={'saved': serializer.data},
            status=status.HTTP_200_OK
        )
