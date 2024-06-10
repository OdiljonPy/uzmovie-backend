from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import LoginView, AuthenticateViewSet, ResendAndResetViewSet, UpdatePasswordViewSet


urlpatterns = [
    path('login/', LoginView.as_view({"post": "login"})),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('register/', AuthenticateViewSet.as_view({"post": "register"})),
    path('register-verify/', AuthenticateViewSet.as_view({"post": "verify_register"})),
    path('resend-otp/', ResendAndResetViewSet.as_view({"get": "resend_otp_code"})),
    path('reset-password/', ResendAndResetViewSet.as_view({'post':'reset_password'})),
    path('reset-password-verify/', ResendAndResetViewSet.as_view({'post':'verify_reset_password'})),
    path('update-password/', UpdatePasswordViewSet.as_view({'post':'update_password'}))

]