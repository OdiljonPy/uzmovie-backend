from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import LoginView, AuthenticateViewSet, ResendAndResetViewSet


urlpatterns = [
    path('login/', LoginView.as_view({"post": "login"})),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('register/', AuthenticateViewSet.as_view({"post": "register"})),
    path('register-verify/', AuthenticateViewSet.as_view({"post": "verify_register"})),
    path('resend-otp/', ResendAndResetViewSet.as_view({"get": "resend_otp_code"}))
]
