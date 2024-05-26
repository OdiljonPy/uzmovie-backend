from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from .models import *
from .serializers import *


class AuthenticateViewSet(ViewSet):
    # def register(self, request, *args, **kwargs):
    #     username = request.data.get('username')
    #     password = request.data.get('password')
    #     serializer = UserSerializer(data={'username': username, 'password': password})
    #     if serializer.is_valid():
    #         serializer.validated_data['is_verified'] = False
    #         serializer.save()
    #         return Response(data=)

    def verify_register(self, request, *args, **kwargs):
        pass

    def login(self, request, *args, **kwargs):
        pass


class ResendAndResetViewSet(ViewSet):
    def reset_password(self, request, *args, **kwargs):
        pass

    def verify_reset_password(self, request, *args, **kwargs):
        pass

    def resend_otp_code(self, request, *args, **kwargs):
        pass

