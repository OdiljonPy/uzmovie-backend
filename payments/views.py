from datetime import timedelta
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from django.utils import timezone
from datetime import date

from authentication.models import User
from config import settings
from .models import Card, ChoiceOTP, Balance_service, Subscription, Choice, Status
from rest_framework import status
from .utils import send_otp_telegram, expiring_date

class BuySubscriptionViewSet(ViewSet):

    def info(self, request, *args, **kwargs):
        phone_number = request.data.get('phone_number')
        token = request.data.get('token')
        choice_status = kwargs.get('choice')

        choice = Choice.objects.filter(name=choice_status).first()
        card = Card.objects.filter(phone_number=phone_number, token=token).first()

        if card is None:
            return Response(data="not found", status=status.HTTP_404_NOT_FOUND)

        otp = ChoiceOTP.objects.create(phone_number=card.phone_number, choice=choice)
        otp.save()

        send_otp_telegram(otp)

        return Response(data={'otp_key': otp.otp_key}, status=status.HTTP_201_CREATED)

    def verify(self, request, *args, **kwargs):
        otp_code = request.data.get('otp_code')
        phone_number = request.data.get('phone_number')
        otp = ChoiceOTP.objects.filter(otp_code=otp_code).first()
        choice = Choice.objects.filter(name=otp.choice).first()
        user_obj = User.objects.filter(username=phone_number).first()
        card = Card.objects.filter(phone_number=phone_number).first()
        service_balance = Balance_service.objects.filter(merchant_id=12345).first()
        statusOTP = Status.objects.filter(name="active").first()

        if otp is None:
            return Response(data="otp code is wrong", status=status.HTTP_400_BAD_REQUEST)

        if (timezone.now() - otp.created_at) > timedelta(minutes=3):
            return Response(data="otp code is expired", status=status.HTTP_400_BAD_REQUEST)

        price = choice.price

        assert card.balance > price, ValueError("Balance should be grater than amount")

        card.balance -= price
        card.save(update_fields=['balance'])

        service_balance.balance += price
        service_balance.save(update_fields=['balance'])

        subscription = Subscription.objects.filter(user=user_obj).first()


        if subscription is None:
            year = date.today().year
            month = date.today().month
            day = date.today().day + 2

            expired_at = date(year, month, day)
            subscription_create = Subscription.objects.create(user=user_obj, choice=choice, status=statusOTP, expired_at=expired_at)
            subscription_create.save()
            return Response(data={"successfuly subscribed"}, status=status.HTTP_200_OK)


        sub_expired_at = subscription.expired_at
        year = sub_expired_at.year
        month = sub_expired_at.month
        day = sub_expired_at.day

        subs_expired_at = expiring_date(year, month, day)

        subscription.choice = choice
        subscription.status = statusOTP
        subscription.expired_at = subs_expired_at
        subscription.save(update_fields=['choice', 'status', 'expired_at'])

        otp.delete()

        return Response(data={"successfuly updated subscription"}, status=status.HTTP_200_OK)

