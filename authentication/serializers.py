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
        fields = ('username', 'first_name', 'last_name', 'profile_picture', 'is_verified', 'is_active')


class UserRequestSerializer(Serializer):
    username = serializers.CharField(max_length=12, validators=[username_validation])
    password = serializers.CharField(max_length=50)


class LoginSerializer(TokenObtainSerializer):
    def validate(self, attrs):
        if self.user.is_verified:
            data = super().validate(attrs)
            return data
        else:
            raise ValidationError("User is not verified")


class OTPRegisterResendSerializer(ModelSerializer):
    class Meta:
        model = OTPRegisterResend
        fields = ('otp_key', )


class OTPRegisterResendRequestSerializer(Serializer):
    otp_code = serializers.IntegerField()
