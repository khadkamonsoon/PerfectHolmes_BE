from rest_framework import serializers
from api.exceptions import CustomValidationError
from api.validator import UsernameValidator, NicknameValidator
from .models import User


class SignupSerializer(serializers.Serializer):
    username = serializers.CharField()
    nickname = serializers.CharField()
    phone_number = serializers.CharField(required=False)
    password = serializers.CharField(min_length=8)
    password2 = serializers.CharField(min_length=8)

    def validate(self, data):
        if data["password"] != data["password2"]:
            raise CustomValidationError({"data": "비밀번호가 일치하지 않습니다."})
        return data

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise CustomValidationError({"data": "이미 존재하는 아이디입니다."})
        return value

    def validate_nickname(self, value):
        if User.objects.filter(nickname=value).exists():
            raise CustomValidationError({"data": "이미 존재하는 닉네임입니다."})
        return value

    def validate_password(self, value):
        return value


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class RefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ("password",)
