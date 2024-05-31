from django.urls import path
from .views import BuySubscriptionViewSet

urlpatterns = [
    path('info/<str:choice>', BuySubscriptionViewSet.as_view({"post": 'info'})),
    path('verify/', BuySubscriptionViewSet.as_view({"post": 'verify'})),
]




