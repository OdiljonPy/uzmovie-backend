from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from .models import Movie, Comment
from .serializers import MovieSerializer, CommentSerializer
from payments.utils import check_status


def check_premium(user, movie_id):
    movie = Movie.objects.filter(id=movie_id).first()
    if movie is None:
        return Response(data={'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)

    is_premium = check_status(user, movie)
    if not is_premium.data == {'ok': True}:
        return Response(
            status=status.HTTP_400_BAD_REQUEST,
            data={'detail': 'This movie is only for premium users'}
        )

    comments = Comment.objects.filter(movie_id=movie.id)
    comment_serializer = CommentSerializer(comments, many=True)

    genres = movie.genres.all()
    actors = movie.actors.all()
    directors = movie.directors.all()

    recommendations = Movie.objects.filter(
        Q(genres__in=genres) | Q(actors__in=actors) | Q(directors__in=directors)
    ).exclude(id=movie.id).distinct()[:5]

    recommendation_serializer = MovieSerializer(recommendations, many=True)

    return Response(
        status=status.HTTP_200_OK,
        data={
            'movie': MovieSerializer(movie).data,
            'comments': comment_serializer.data,
            'recommendation': recommendation_serializer.data
        }
    )
