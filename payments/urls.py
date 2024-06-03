from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import BuySubscriptionViewSet, VerifyOTPViewSet, GetChoicesViewSet

urlpatterns = [
    path('', GetChoicesViewSet.as_view({"get": 'choices'})),
    path('info/', BuySubscriptionViewSet.as_view({"post": 'info'})),
    path('verify/', VerifyOTPViewSet.as_view({"post": 'verify'}),),
]


