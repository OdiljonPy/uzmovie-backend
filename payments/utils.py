from authentication.models import User
from movie.models import Movie
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



def validate_move(user_id, movie_id):

    from .models import Subscription, Status

    user = User.objects.filter(id=user_id).first()
    movie = Movie.objects.filter(id=movie_id).first()
    subscription = Subscription.objects.filter(user=user)
    status = Status.objects.filter(name='active')

    if movie.premium_status is False:
        return True

    elif subscription.status == status:
        return True
    else:
        return False

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

def validated_uz_phone_number(phone_number: str):
    phone_number = phone_number.replace(' ', '')
    if len(phone_number) != 12:
        raise ValidationError('Length should be 12')
    if not phone_number.startswith('998'):
        raise ValidationError('Phone number should starts with 998')
    if not phone_number[1:].isdigit():
        raise ValidationError('Phone number should consists of digits (0-9)')


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



