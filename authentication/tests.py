import re
from django.core.exceptions import ValidationError

number_codes = ('99', '98', '97', '95', '94', '93', '91', '90', '77', '55', '33', '71')


def username_validation(username):
    # Combine the number codes into a single regular expression pattern
    pattern = r'^998(' + '|'.join(number_codes) + r')\d{7}$'

    if re.match(pattern, username):
        return True
    raise ValidationError('Username should be an Uzbek phone number')


# Example usage
try:
    username_validation('998771234567')
    print("Valid username")
except ValidationError as e:
    print(e)