from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from .models import Movie, Saved, Comment
from rest_framework import status
from .serializers import MovieSerializer, CommentSerializer, SavedSerializer
from rest_framework.permissions import IsAuthenticated
from authentication.models import User
from payments.utils import check_status


class SearchViewSet(ViewSet):
    @swagger_auto_schema(
        operation_description="Search movie by name",
        operation_summary="Search movie by name",
        manual_parameters=[
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
        movies = Movie.objects.filter(title__icontains=search)  # faqat namesi bo`yicha search
        serializer = MovieSerializer(movies, many=True)

        if movies is None:
            return Response(data=serializer.data, status=status.HTTP_404_NOT_FOUND)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class MovieViewSet(ViewSet):
    serializer_class = MovieSerializer

    @swagger_auto_schema(
        operation_description="Filter Movies",
        operation_summary="Filter Movies",
        manual_parameters=[
            openapi.Parameter('title', type=openapi.TYPE_STRING, description='title', in_=openapi.IN_QUERY),
            openapi.Parameter('actor', type=openapi.TYPE_STRING, description='actor', in_=openapi.IN_QUERY),
            openapi.Parameter('director', type=openapi.TYPE_STRING, description='director', in_=openapi.IN_QUERY),
            openapi.Parameter('genre', type=openapi.TYPE_STRING, description='genre', in_=openapi.IN_QUERY),
            openapi.Parameter('country', type=openapi.TYPE_STRING, description='country', in_=openapi.IN_QUERY),
            openapi.Parameter('release_date', type=openapi.TYPE_INTEGER, description='release_date', in_=openapi.IN_QUERY),
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
        elif data.get("country"):
            movies = Movie.objects.filter(countries__name__contains=data['country'])
        elif data.get("release_date"):
            movies = Movie.objects.filter(release_date__contains=data['release_date'])
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
        user = request.user
        if not request.user.is_authenticated:
            return Response(data={'error': 'Not authenticated'}, status=status.HTTP_404_NOT_FOUND)

        movie = Movie.objects.filter(id=kwargs['pk']).first()
        if movie is None:
            return Response(data={'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
        is_premium = check_status(user, movie)
        if is_premium.data == {'ok': True}:
            comment = Comment.objects.filter(movie_id=movie)
            serializer = CommentSerializer(comment, many=True)
            return Response(
                status=status.HTTP_200_OK,
                data={
                    'movie': MovieSerializer(movie).data,
                    'comments': serializer.data
                })
        return Response(
            status=status.HTTP_400_BAD_REQUEST,
            data={'detail': 'This movie only for premium users'}
        )


class CommentViewSet(ViewSet):
    # review
    @swagger_auto_schema(
        operation_description="Review Comment by id",
        operation_summary="Review Comment by id",
        manual_parameters=[
            openapi.Parameter(
                'id', type=openapi.TYPE_INTEGER, description='Comment id', in_=openapi.IN_QUERY, required=True
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
                'movie id', type=openapi.TYPE_INTEGER, description='movie id', in_=openapi.IN_QUERY, required=True),
            openapi.Parameter(
                'content', type=openapi.TYPE_STRING, description='message', in_=openapi.IN_QUERY, required=True),
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
        movie = Movie.objects.filter(id=request.data['movie']).first()
        user = request.user

        if not request.user.is_authenticated:
            return Response(data={'error': 'Not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)

        request.data['user'] = user.id
        serializer = CommentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.validated_data['user'] = myuser_id
            comment = Comment.objects.filter(author=user, movie=movie, rating__gt=0).first()
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

        elif comment.user != request.user:
            return Response(
                data={'error': 'You do not have permission to delete this comment'}, status=status.HTTP_400_BAD_REQUEST
            )
        comment.delete()
        r_movie = Movie.objects.filter(id=comment.movie_id).first()
        comments = Comment.objects.filter(
            movie=comment.movie_id, rated=True
        )
        if comments == []:
            s = 0
            l = 0
            for comment in comments:
                s += comment.rating
                l += 1

            r_movie.p_rating = s / l
            r_movie.save(update_fields=['p_rating'])
            return Response(data={'message': 'Successfully deleted'}, status=status.HTTP_200_OK)

        r_movie.p_rating = 0
        r_movie.save(update_fields=['p_rating'])
        return Response(data={'message': 'Successfully deleted'}, status=status.HTTP_200_OK)


class SavedViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Saved movie by id",
        operation_summary="Saved movie by id",
        manual_parameters=[
            openapi.Parameter('saved', type=openapi.TYPE_INTEGER, description='saved', in_=openapi.IN_QUERY),
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
        my_user = User.objects.filter(id=request.user.id).first()
        if not my_user:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={'detail': 'User not found'},
            )

        movie = Movie.objects.filter(id=kwargs['pk']).first()
        if not movie:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={'detail': 'Movie not found'},
            )

        save = Saved.objects.filter(user=my_user, movie=movie).first()
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

    @swagger_auto_schema(
        operation_description="Saved movie list",
        operation_summary="Saved movie list",
        responses={
            200: MovieSerializer(),
            404: 'Not found'
        },
        tags=['movie']
    )
    def list_movie(self, request, *args, **kwargs):
        user = request.user
        save = Saved.objects.filter(user=user)
        serializer = SavedSerializer(save, many=True)
        return Response(
            data={'saved': serializer.data},
            status=status.HTTP_200_OK
        )
