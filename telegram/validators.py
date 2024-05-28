from django.core.exceptions import ValidationError


def validate_username(username):
    if not username.startwith('@'):
        raise ValidationError("Username must be started with @")
