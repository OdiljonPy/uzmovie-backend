from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer
from .models import ChoiceOTP, Subscription


class SubscriptionSerializer(ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'


class CardPanSerializer(Serializer):
    pan = serializers.IntegerField()


class ChoiceOTPSerializer(ModelSerializer):
    class Meta:
        model = ChoiceOTP
        fields = ("otp_key",)

