from rest_framework import serializers

PASSWORD_MATCH_ERROR_MESSAGE = "Passwords do not match."
PASSWORD_ERROR_MESSAGE = ("Password must be at least 8 characters long and"
                          " contain at least one digit and one special character.")


def validate_password_match(password, confirm_password):
    if password and confirm_password and password != confirm_password:
        raise serializers.ValidationError({"Password_error": PASSWORD_MATCH_ERROR_MESSAGE})


def validate_password(value):
    if (len(value) < 8 or not any(char.isdigit() for char in value)
            or not any(char in '!@#$%^&*(),.?":{}|<>' for char in value)):
        raise serializers.ValidationError({"Password_errors": PASSWORD_ERROR_MESSAGE})
