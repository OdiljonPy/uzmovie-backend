from django.urls import path
from .views import BuySubscriptionViewSet

urlpatterns = [
    path('info/', BuySubscriptionViewSet.as_view({"post": 'info'})),
    path('verify/', BuySubscriptionViewSet.as_view({"post": 'verify'})),
]




