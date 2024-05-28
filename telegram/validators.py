from django.core.exceptions import ValidationError


def validate_username(username):
    if not username.startswith('@'):
        raise ValidationError("Username must be started with @")
