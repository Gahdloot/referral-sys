import re
from rest_framework import serializers

def validate_phone_number(phone_number):
    """
    Validate phone number using regular expression
    """
    if phone_number:
        phone_regex = re.compile(r'^\d{11}$')
        result = phone_regex.match(phone_number)
        if not result:
            raise serializers.ValidationError(f'{phone_number} is not a valid phone number')
        # print(result.group())
        return phone_number


# print(validate_phone_number('0803955086'))