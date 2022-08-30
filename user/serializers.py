from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from .models import User


class ResisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'is_verify')
        extra_kwargs = {'password': {'write_only': True}, 'is_verify': {'read_only': True}}

    def create(self, validated_data):
        return self.Meta.model.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):  # noqa
    username = serializers.CharField(max_length=150, required=True, write_only=True)
    password = serializers.CharField(max_length=150, required=True, write_only=True)
    token = serializers.CharField(read_only=True, max_length=255)

    def create(self, validated_data):
        user = authenticate(**validated_data)
        if not user:
            raise AuthenticationFailed()
        if not user.is_verify:
            raise AuthenticationFailed('User not verified')
        return user
