from django.urls import path

from .views import MovieViewSet, CommentViewSet, SavedViewSet, SearchViewSet

urlpatterns = [
    # SEARCH
    path('search/', SearchViewSet.as_view({'post': 'search'})),

    # MOVIE
    path('movies/', MovieViewSet.as_view({'get': 'filter'})),
    path('movie/<int:pk>/', MovieViewSet.as_view({'get': 'get_by_id'})),
  
    # SAVED
    path('save/movie/<int:pk>/', SavedViewSet.as_view({'post': 'save_movie'})),
    path('save/list/', SavedViewSet.as_view({'get': 'list_movie'})),

    # COMMENT
    path('comment/', CommentViewSet.as_view({'post': 'comment_create'})),
    path('comment/<int:pk>/', CommentViewSet.as_view({'delete': 'comment_destroy'})),
    path('comment/<int:pk>/', CommentViewSet.as_view({'get': 'comment_review'})),
]
