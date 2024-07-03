from django.urls import path

from .views import (
    MovieListCreateViewSet, CommentListCreateViewSet, UtilsViewSet,
)

urlpatterns = [

    # Movies
    path('', MovieListCreateViewSet.as_view({'get': 'list_movies'})),
    path('<int:pk>/', MovieListCreateViewSet.as_view({'get': 'retrieve_movie'})),

    # Comments
    path('comments/', CommentListCreateViewSet.as_view({'get': 'list_comments'})),
    path('comment/', CommentListCreateViewSet.as_view({'post': 'create_comment'})),

    # Utils
    path('pagination/', UtilsViewSet.as_view({'post': 'pagination'})),
    path('search/', UtilsViewSet.as_view({'post': 'search'})),
    path('rating/', UtilsViewSet.as_view({'post': 'rating'})),
    path('saved/', UtilsViewSet.as_view({'post': 'saved'})),

]
