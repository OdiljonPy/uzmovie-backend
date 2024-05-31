from django.urls import path

from .views import MovieViewSet, SavedViewSet, AuthViewSet

urlpatterns = [
    path('movies/', MovieViewSet.as_view({'get': 'filter'})),
    path('movies/<int:pk>/', MovieViewSet.as_view({'get': 'get_by_id'})),

    path('saved/', SavedViewSet.as_view({'get': 'get'})),
    path('saved/add/', SavedViewSet.as_view({'post': 'post'})),

    path('register/', AuthViewSet.as_view({'post': 'register'})),
]
