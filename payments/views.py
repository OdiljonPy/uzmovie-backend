from datetime import timedelta, date
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.utils import timezone
from authentication.models import User
from .models import Card, ChoiceOTP, Subscription, Choice
from .serializers import SubscriptionSerializer, ChoiceOTPSerializer, CardPanSerializer, OTPCodeSerializer, ChoiceSerializer
from rest_framework import status, throttling
from drf_yasg.utils import swagger_auto_schema
from .utils import send_otp_telegram, expiring_date


class GetChoicesViewSet(ViewSet):
    @swagger_auto_schema(
        operation_description="info",
        operation_summary="Get Choices",
        responses={200: ChoiceSerializer()},
        tags=['payment']
    )

    def choices(self, request, *args, **kwargs):
        choices = Choice.objects.all()
        serializer = ChoiceSerializer(choices, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

class BuySubscriptionViewSet(ViewSet):
    permission_classes = [IsAuthenticated, AllowAny]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        operation_description="info",
        operation_summary="get card number",
        responses={201: ChoiceOTPSerializer()},
        request_body=CardPanSerializer(),
        tags=['payment']

    )

    def info(self, request, *args, **kwargs):
        user = request.user

        if user.is_authenticated:
            pan = request.data.get('pan')
            choice_status = request.data.get('choice')

            choice = Choice.objects.filter(name=choice_status).first()
            card = Card.objects.filter(pan=pan).first()

            if card is None:
                return Response(data="card not found", status=status.HTTP_404_NOT_FOUND)
            if choice is None:
                return Response(data="choice not found", status=status.HTTP_404_NOT_FOUND)
            if card.balance < choice.price:
                return Response(data="not enough money", status=status.HTTP_404_NOT_FOUND)

            otp = ChoiceOTP.objects.create(user=user, phone_number=card.phone_number, choice=choice)
            otp.save()

            send_otp_telegram(otp)

            return Response(data={'otp_key': otp.otp_key}, status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_401_UNAUTHORIZED)

class VerifyOTPViewSet(ViewSet):
    permission_classes = [AllowAny]
    authentication_classes = [JWTAuthentication]

    throttle_scope = 'verify_otp'

    @swagger_auto_schema(
        operation_description="verify",
        operation_summary="verify transaction",
        responses={201: SubscriptionSerializer()},
        request_body=OTPCodeSerializer(),
        tags=['payment']
    )
    def verify(self, request, *args, **kwargs):
        otp_key = request.data.get('otp_key')
        otp_code = request.data.get('otp_code')
        otp = ChoiceOTP.objects.filter(otp_key=otp_key).first()

        if otp is None:
            return Response(data="otp code is wrong", status=status.HTTP_400_BAD_REQUEST)

        choice = Choice.objects.filter(name=otp.choice.name).first()
        user_obj = User.objects.filter(username=otp.user).first()

        if (timezone.now() - otp.created_at) > timedelta(minutes=3):
            otp.delete()
            return Response(data="otp code is expired", status=status.HTTP_400_BAD_REQUEST)

        if otp.otp_code != otp_code:
            return Response(data="otp code is wrong", status=status.HTTP_400_BAD_REQUEST)

        subscription = Subscription.objects.filter(user=user_obj).first()

        if subscription is None:
            year = date.today().year
            month = date.today().month + 1
            day = date.today().day

            expired_at = date(year, month, day)
            subscription_create = Subscription.objects.create(user=user_obj, choice=choice, status=1, expired_at=expired_at)
            subscription_create.save()
            otp.delete()
            return Response(data={"successfully subscribed"}, status=status.HTTP_200_OK)

        sub_expired_at = subscription.expired_at
        year = sub_expired_at.year
        month = sub_expired_at.month
        day = sub_expired_at.day

        subs_expired_at = date(year, month, day)

        subscription.choice = choice
        subscription.status = '1'
        subscription.expired_at = subs_expired_at
        subscription.save(update_fields=['choice', 'status', 'expired_at'])

        otp.delete()

        return Response(data={"successfully updated subscription"}, status=status.HTTP_200_OK)
