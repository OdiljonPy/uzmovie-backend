import requests
from django.core.exceptions import ValidationError
from django.conf import settings

BOT_ID = settings.BOT_ID
CHAT_ID = settings.CHAT_ID
TELEGRAM_API_URL = settings.TELEGRAM_API_URL


def send_message_telegram(obj):
    message = (f"Project:Uzmovi\n"
               f"phone_number:{obj.phone_number}\n"
               f"first_name:{obj.first_name}\n"
               f"last_name:{obj.last_name}\n"
               f"email:{obj.email}\n"
               f"message:{obj.message}"
               )
    return requests.get(TELEGRAM_API_URL.format(BOT_ID, message, CHAT_ID))


def phone_number_validation(phone_number):
    if len(phone_number) == 13 and phone_number[:4] == '+998' and phone_number[1:13].isdigit():
        return True
    raise ValidationError('phone_number is invalid')
