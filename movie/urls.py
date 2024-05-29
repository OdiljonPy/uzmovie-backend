from django.urls import path
from .views import MovieViewSet, SavedViewSet, CommentViewSet, SearchAPIView

urlpatterns = [
    # SEARCH
    path('search/', SearchAPIView.as_view()),
    # MOVIE
    path('get-all/', MovieViewSet.as_view({'get': 'get_all'})),
    path('by-id/', MovieViewSet.as_view({'get': 'get_by_id'})),
    path('by-genre/', MovieViewSet.as_view({'get': 'get_by_genre'})),
    path('by-director/', MovieViewSet.as_view({'get': 'get_by_director'})),
    path('by-actor/', MovieViewSet.as_view({'get': 'get_by_actor'})),
    # SAVED
    path('save/', SavedViewSet.as_view({'post': 'save_movie'})),
    # COMMENT
    path('comment/create/', CommentViewSet.as_view({'post': 'comment_create'})),
    path('comment/delete/<int:pk>/', CommentViewSet.as_view({'delete': 'comment_destroy'})),
    path('comment/review/<int:pk>/', CommentViewSet.as_view({'get': 'comment_review'})),
    path('comment/list/', CommentViewSet.as_view({'get': 'comment_list'})),

]
