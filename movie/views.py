from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from .models import Movie, Actor, Director, Genre, Saved, Comment
from rest_framework import status, filters
from .serializers import MovieSerializer, SearchSerializer, CommentSerializer
from rest_framework.permissions import IsAuthenticated
from authentication.models import User


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
        movies = Movie.objects.filter(name__icontains=search) # faqat (name)i bo`yicha search
        serializer = MovieSerializer(movies, many=True)
        if movies is None:
            return Response(data={'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

        return Response(data={'movies': serializer.data}, status=status.HTTP_200_OK)


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


class CommentViewSet(ViewSet):
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

