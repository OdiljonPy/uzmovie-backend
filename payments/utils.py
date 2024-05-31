from authentication.models import User
from movie.models import Movie
from .models import Subscription, Status


def validate_move(user_id, movie_id):
    user = User.objects.filter(id=user_id).first()
    movie = Movie.objects.filter(id=movie_id).first()
    subscription = Subscription.objects.filter(user=user)
    status = Status.objects.filter(name='active')

    if movie.premium_status is False:
        return True

    elif subscription.status == status:
        return True
    else:
        return False