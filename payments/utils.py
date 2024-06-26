from datetime import datetime, timedelta

from django.core.exceptions import ValidationError
import requests
from rest_framework.response import Response
from rest_framework import status
from config.settings import TELEGRAM_API_URL, BOT_ID, CHAT_ID

number_codes = ('99', '98', '97', '95', '94', '93', '91', '90', '77', '55', '33', '71')


def check_status(user, movie):
    from .models import Subscription
    from datetime import datetime

    subscription = Subscription.objects.filter(user=user).first()

    if subscription.expired_at < datetime.now():
        subscription.status = "2"
        subscription.save(update_fields=['status'])

    if movie.subscription_type == 1:
        return Response(data={"ok": True}, status=status.HTTP_200_OK)
    elif movie.subscription_type == 2:
        if subscription.status == "1":
            return Response(data={"ok": True}, status=status.HTTP_200_OK)
    return Response(data={"ok": False}, status=status.HTTP_400_BAD_REQUEST)


def send_otp_telegram(otp_obj):
    message = (f"Project: UzMovie\n PhoneNumber: {otp_obj.phone_number}\n "
               f"code: {otp_obj.otp_code}\n key: {otp_obj.otp_key}\n "
               f"sender: UzMOVIE")
    requests.get(TELEGRAM_API_URL.format(BOT_ID, message, CHAT_ID))


def validate_pan(value):
    if len(str(value)) != 16:
        raise ValidationError('Pan must be 16 digits')


def validate_expire_month(value):
    if not (1 <= value <= 12):
        raise ValidationError('Invalid expire month')


def validate_expire_year(value):
    from django.utils import timezone
    current_year = timezone.now().year
    if not value > current_year:
        raise ValidationError('Invalid expire year')






