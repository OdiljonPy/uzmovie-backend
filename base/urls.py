from django.urls import path
from .views import ContactViewSet, AboutViewSet

from .views import ContactViewSet

urlpatterns = [
    # contact
    path('contact/list/', ContactViewSet.as_view({'get': 'contact_list'})),
    path('contact/create/', ContactViewSet.as_view({'post': 'contact_create'})),

    # about us
    path('list/', AboutViewSet.as_view({'get': 'about_view'}))
    path('contact_list/', ContactViewSet.as_view({'get': 'contact_list'})),
    path('contact_create/', ContactViewSet.as_view({'post': 'contact_create'}))
]
