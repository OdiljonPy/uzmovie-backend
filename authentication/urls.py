from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import LoginView, AuthenticateViewSet, ResendAndResetViewSet

urlpatterns = [
    path('login/', LoginView.as_view({"post": "login"})),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('auth-me/', LoginView.as_view({"get": "auth_me"})),
    path('user-update/', LoginView.as_view({"patch": "profile_update"})),
    path('register/', AuthenticateViewSet.as_view({"post": "register"})),
    path('register/verify/', AuthenticateViewSet.as_view({"post": "verify_register"})),
    path('otp/resend/', ResendAndResetViewSet.as_view({"post": "resend_otp_code"})),
    path('password/reset/', ResendAndResetViewSet.as_view({"post": "reset_password"})),
    path('password/reset/verify/', ResendAndResetViewSet.as_view({"post": "verify_reset_password"})),
    path('set/password/', ResendAndResetViewSet.as_view({"patch": "set_new_password"}))
]
