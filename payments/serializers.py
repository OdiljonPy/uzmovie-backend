from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer
from .models import ChoiceOTP, Subscription, Choice


class SubscriptionSerializer(ModelSerializer):
    class Meta:
        model = Subscription
        fields = ("id", "user", "choice", "status", "start_date", "expired_at")


class ChoiceSerializer(ModelSerializer):
    class Meta:
        model = Choice
        fields = ("id", "name", "price", "description")


class OTPCodeSerializer(Serializer):
    otp_key = serializers.IntegerField()
    otp_code = serializers.IntegerField()


class CardPanSerializer(Serializer):
    pan = serializers.IntegerField()
    choice = serializers.IntegerField()


class ChoiceOTPSerializer(ModelSerializer):
    class Meta:
        model = ChoiceOTP
        fields = ("otp_key",)


class DeleteChoiceOTPSerializer(ModelSerializer):
    class Meta:
        model = ChoiceOTP
        fields = ("id", "otp_key", "otp_code", "choice", "user", "phone_number", "created_at")



