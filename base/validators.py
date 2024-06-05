from rest_framework.exceptions import ValidationError


def validate_uz_phone_number(phone_number: str):
    phone_number = phone_number.replace('', '')
    if len(phone_number) != 13:
        raise ValidationError('Phone number length must be 13')
    if not phone_number.startswith('+998'):
        raise ValidationError('Phone number must start with +998')
    if not phone_number[1:].isdigit():
        raise ValidationError('Phone number must be  digital numbers')

