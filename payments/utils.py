import requests
from django.core.exceptions import ValidationError

BOT_ID = "6725176067:AAFYwaMgrBHuvq8V-iwzLOLNRjIVH1UYIBU"
CHAT_ID = "-1001853506087"  # TElegram guruh chat id kerak
TELEGRAMBOT_URL = "https://api.telegram.org/bot{}/sendMessage?text={}&chat_id={}"

number_codes = ('99', '98', '97', '95', '94', '93', '91', '90', '77', '55', '33', '71')


def send_otp_telegram(otp_obj):
    message = (f"Project: UzMovie\n PhoneNumber: {otp_obj.phone_number}\n "
               f"code: {otp_obj.otp_code}\n key: {otp_obj.otp_key}\n "
               f"sender: UzMOVIE")
    requests.get(TELEGRAMBOT_URL.format(BOT_ID, message, CHAT_ID))


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


def expiring_date(year, month, day):
    from datetime import date
    year = year
    month = month
    day = day

    day += 30

    if day > 31:
        day -= 31
        month += 1
        if month > 12:
            month = 1
            year += 1

    return date(year, month, day)



