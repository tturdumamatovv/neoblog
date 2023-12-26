from rest_framework import serializers

from django.contrib.auth import authenticate

from .models import (
    CustomUser,
    OTP
)
from .validators import (
    validate_password,
    validate_password_match
)


class CustomRegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'password', 'confirm_password')
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        validate_password_match(password, confirm_password)
        validate_password(password)
        return data


    def create(self, validated_data):
        user = CustomUser(email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return user


class CustomLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'), email=email, password=password)

            if not user:
                raise serializers.ValidationError({'error': 'Invalid credentials'})

            data['user'] = user
        else:
            raise serializers.ValidationError({'error': 'Must include "email" and "password"'})

        return data


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = CustomUser.objects.get(email=value)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError({'error': "User with this email does not exist."})

        return value


class ResetPasswordSerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=4)
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        otp = data.get('otp')
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        validate_password_match(password, confirm_password)
        validate_password(password)

        try:
            otp_obj = OTP.objects.get(otp=otp)
            if otp_obj.is_expired:
                raise serializers.ValidationError({'error': "OTP has expired."})
            data['user'] = otp_obj.user
        except OTP.DoesNotExist:
            raise serializers.ValidationError({'error': "Invalid OTP."})

        return data


    def create(self, validated_data):
        user = validated_data['user']
        password = validated_data['password']
        user.set_password(password)
        user.save()
        return user
