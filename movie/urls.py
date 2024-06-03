from django.urls import path

from .views import MovieViewSet, CommentViewSet, SavedViewSet, SearchViewSet

urlpatterns = [
    # SEARCH
    path('search/', SearchViewSet.as_view({'get': 'search'})),

    # MOVIE
    path('movies/', MovieViewSet.as_view({'get': 'filter'})),
    path('movie/<int:pk>/', MovieViewSet.as_view({'get': 'get_by_id'})),
  
    # SAVED
    path('save/movie/<int:pk>/', SavedViewSet.as_view({'post': 'save_movie'})),
    path('save/list/', SavedViewSet.as_view({'get': 'list_movie'})),

    # COMMENT
    path('comment/create/', CommentViewSet.as_view({'post': 'comment_create'})),
    path('comment/delete/<int:pk>/', CommentViewSet.as_view({'delete': 'comment_destroy'})),
    path('comment/review/<int:pk>/', CommentViewSet.as_view({'get': 'comment_review'})),
    path('comment/list/', CommentViewSet.as_view({'get': 'comment_list'})),

]
