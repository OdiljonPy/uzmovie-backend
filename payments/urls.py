from django.urls import path
from .views import BuySubscriptionViewSet, VerifyOTPViewSet

urlpatterns = [
    path('info/<str:choice>/', BuySubscriptionViewSet.as_view({"post": 'info'})),
    path('verify/', VerifyOTPViewSet.as_view({"post": 'verify'})),
]




