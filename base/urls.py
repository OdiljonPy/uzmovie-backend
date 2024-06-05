from django.urls import path
from .views import ContactViewSet, AboutViewSet
urlpatterns = [
    # contact
    path('contact/', ContactViewSet.as_view({'post': 'contact_create'})),

    # about us
    path('about/', AboutViewSet.as_view({'get': 'about'})),
]
