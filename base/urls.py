from django.urls import path
from .views import ContactViewSet, AboutViewSet

urlpatterns = [
    # contact
    path('contact/list/', ContactViewSet.as_view({'get': 'contact_list'})),
    path('contact/create/', ContactViewSet.as_view({'post': 'contact_create'})),

    # about us
    path('about/', AboutViewSet.as_view({'get': 'about_view'})),
]
