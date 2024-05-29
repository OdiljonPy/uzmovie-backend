from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import LoginView, AuthenticateViewSet


urlpatterns = [
    path('login/', LoginView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('register/', AuthenticateViewSet.as_view({"post": "register"})),
    # path('reset-password/'),
    path('reset-password-verify/', AuthenticateViewSet.as_view({"post": "verify_register"})),
]
