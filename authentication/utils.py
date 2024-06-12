import random
from datetime import datetime, timedelta
import requests
from django.core.exceptions import ValidationError

BOT_ID = "6725176067:AAFYwaMgrBHuvq8V-iwzLOLNRjIVH1UYIBU"
CHAT_ID = "1001778810"  # TElegram guruh chat id kerak
TELEGRAMBOT_URL = "https://api.telegram.org/bot{}/sendMessage?text={}&chat_id={}"

number_codes = ('99', '98', '97', '95', '94', '93', '91', '90', '77', '55', '33', '71')


def send_otp_code_telegram(otp_obj):
    message = (f"Project: UzMovie\n PhoneNumber: {otp_obj.otp_user.username}\n "
               f"code: {otp_obj.otp_code}\n key: {otp_obj.otp_key}\n "
               f"sender: UzMOVIE")
    response = requests.get(TELEGRAMBOT_URL.format(BOT_ID, message, CHAT_ID))
    return response


def generate_otp_code():
    return random.randint(10000, 99999)


def check_code_expire(created_at):
    current_time = datetime.now()
    if current_time - created_at > timedelta(minutes=3):
        return False
    return True


def username_validation(username):
    if len(username) == 12 and username[:3] == '998' and username[3:5] in number_codes:
        return True
    raise ValidationError('username should be uzbek phone number')


def checking_number_of_otp(checking):
    current_time = datetime.now()
    if len(checking) >= 3:
        obj = checking[0]
        if current_time - obj.created_at < timedelta(hours=12):
            return False
        return 'delete'
    return True


def check_resend_otp_code(created_at):
    current_time = datetime.now()
    if current_time - created_at < timedelta(minutes=1):
        return False
    return True


def check_token_expire(created_at):
    current_time = datetime.now()
    if current_time - created_at < timedelta(minutes=30):
        return False
    return True
