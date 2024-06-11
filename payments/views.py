from datetime import timedelta, datetime
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.utils import timezone
from authentication.models import User
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from .models import Card, ChoiceOTP, Subscription, Choice
from .utils import send_otp_telegram
from .serializers import SubscriptionSerializer, ChoiceOTPSerializer, CardPanSerializer, OTPCodeSerializer, \
    ChoiceSerializer, DeleteChoiceOTPSerializer
from authentication.utils import checking_number_of_otp


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
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    throttle_scope = 'send_otp'

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

            choice = Choice.objects.filter(id=choice_status).first()
            card = Card.objects.filter(pan=pan).first()

            if card is None:
                return Response(data="card not found", status=status.HTTP_404_NOT_FOUND)
            if choice is None:
                return Response(data="choice not found", status=status.HTTP_404_NOT_FOUND)
            if card.balance < choice.price:
                return Response(data="not enough money", status=status.HTTP_400_BAD_REQUEST)

            del_otp = ChoiceOTP.objects.filter(phone_number=card.phone_number)
            if not checking_number_of_otp(del_otp):
                return Response(data="Try again 12 hours later", status=status.HTTP_400_BAD_REQUEST)
            if checking_number_of_otp(del_otp) == 'delete':
                serializer = DeleteChoiceOTPSerializer(del_otp, data={"deleted_at": datetime.now()}, many=True)
                serializer.save()

            otp = ChoiceOTP.objects.create(user=user, phone_number=card.phone_number, choice=choice)
            otp.save()

            send_otp_telegram(otp)

            return Response(data={'otp_key': otp.otp_key}, status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_401_UNAUTHORIZED)


class VerifyOTPViewSet(ViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

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

        if type(otp_code) is not int:
            return Response(data={"please write number"}, status=status.HTTP_400_BAD_REQUEST)

        otp = ChoiceOTP.objects.filter(otp_key=otp_key, otp_code=otp_code).first()

        if otp is None:
            return Response(data="otp key is wrong or not found", status=status.HTTP_400_BAD_REQUEST)

        choice = Choice.objects.filter(name=otp.choice.name).first()
        user_obj = User.objects.filter(username=otp.user).first()

        if (timezone.now() - otp.created_at) > timedelta(minutes=3):
            otp.deleted_at = timezone.now()
            otp.save(update_fields=['deleted_at'])

            return Response(data="otp code is expired", status=status.HTTP_400_BAD_REQUEST)

        if otp.otp_code != otp_code:
            return Response(data="otp code is wrong", status=status.HTTP_400_BAD_REQUEST)

        subscription = Subscription.objects.filter(user=user_obj).first()
        card = Card.objects.filter(phone_number=otp.phone_number).first()

        if subscription is None:

            expired_at = datetime.now() + timedelta(days=30)
            subscription_create = Subscription.objects.create(user=user_obj, choice=choice, status="1",
                                                              expired_at=expired_at)
            subscription_create.save()

            card.balance -= choice.price
            card.save(update_fields=['balance'])

            otp.deleted_at = timezone.now()
            otp.save(update_fields=['deleted_at'])
            return Response(data={"successfully subscribed"}, status=status.HTTP_200_OK)

        subscription.choice = choice
        subscription.status = 1
        subscription.expired_at = subscription.expired_at + timedelta(days=30)
        subscription.save(update_fields=['choice', 'status', 'expired_at'])

        card.balance -= choice.price
        card.save(update_fields=['balance'])

        otp.deleted_at = timezone.now()
        otp.save(update_fields=['deleted_at'])

        return Response(data={"successfully updated subscription"}, status=status.HTTP_200_OK)

