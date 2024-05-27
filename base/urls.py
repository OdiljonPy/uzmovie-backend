from django.urls import path
from .views import ContactViewSet

urlpatterns = [
    path('contact_list/', ContactViewSet.as_view({'get': 'contact_list'})),
    path('contact_create/', ContactViewSet.as_view({'post': 'contact_create'}))
]
