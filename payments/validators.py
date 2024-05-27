from django.utils import timezone
from django.core.exceptions import ValidationError

def validate_pan(value):
    if len(str(value)) != 16:
        raise ValidationError('Pan must be 16 digits')

def validate_expire_month(value):
    if not (1 <= value <= 12):
       raise ValidationError('Invalid expire month')

def validate_expire_year(value):
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



