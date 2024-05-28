from django.urls import path
from .views import MovieViewSet

urlpatterns = [
    path('movies/', MovieViewSet.as_view({'get': 'filter'})),
    path('movie/<int:pk>/', MovieViewSet.as_view({'get': 'get_by_id'})),
]
