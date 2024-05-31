from typing import Dict, Any

from rest_framework.serializers import ModelSerializer, Serializer
from .models import User, OTPRegisterResend
from rest_framework import serializers
from .utils import username_validation
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from django.core.exceptions import ValidationError


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'profile_picture', 'password')
        extra_kwargs = {
            'password': {'write_only': True},
        }


class RegisterUserSerializer(Serializer):
    username = serializers.CharField(max_length=12, validators=[username_validation])
    password = serializers.CharField(max_length=50)


class UpdateUserSerializer(Serializer):
    first_name = serializers.CharField(max_length=100, required=False)
    last_name = serializers.CharField(max_length=100, required=False)
    profile_picture = serializers.ImageField(required=False)


class OTPRegisterResendSerializer(ModelSerializer):
    class Meta:
        model = OTPRegisterResend
        fields = ('otp_key', )


class OTPRegisterVerifySerializer(Serializer):
    otp_code = serializers.IntegerField()
    otp_key = serializers.UUIDField()


class OTPResendSerializer(Serializer):
    otp_key = serializers.UUIDField()


class ResetUserPasswordSerializer(Serializer):
    username = serializers.CharField(max_length=12, validators=[username_validation,])


class SetNewPasswordSerializer(Serializer):
    otp_token = serializers.UUIDField()
    password = serializers.CharField(max_length=20)
    rep_password = serializers.CharField(max_length=20)
