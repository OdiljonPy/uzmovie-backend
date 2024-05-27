import random
from datetime import datetime, timedelta
import requests
from .models import User


BOT_ID = "6725176067:AAFYwaMgrBHuvq8V-iwzLOLNRjIVH1UYIBU"
CHAT_ID = "" # TElegram guruh chat id kerak
TELEGRAMBOT_URL = "https://api.telegram.org/bot{}/sendMessage?text={}&chat_id={}"

number_codes = ('99', '98', '97', '95', '94', '93', '91', '90', '77', '55', '33', '71')


def send_otp_code_telegram(otp_obj):
    message = (f"Project: UzMovie\n PhoneNumber: {otp_obj.user}\n "
               f"code: {otp_obj.otp_code}\n key: {otp_obj.otp_key}\n "
               f"sender: UzMOVIE")
    requests.get(TELEGRAMBOT_URL.format(BOT_ID, message, CHAT_ID))


def generate_otp_code():
    return random.randint(10000, 99999)


def check_code_expire(created_at):
    current_time = datetime.now()
    allowed_minut = timedelta(minutes=3)
    if current_time - created_at > allowed_minut:
        return False
    return True


def username_validation(username):
    if len(username) == 12:
        if username[:3] == '998':
            if username[3:5] in number_codes:
                return True
    return False


def check_for_valideness(email):
    email_is_registered = User.objects.filter(email=email).first()

    if email_is_registered is None:
        return True
    return False

