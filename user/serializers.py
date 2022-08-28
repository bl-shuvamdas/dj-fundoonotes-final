from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework import status

from .models import User


class ResisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return self.Meta.model.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):  # noqa
    username = serializers.CharField(max_length=150, required=True, write_only=True)
    password = serializers.CharField(max_length=150, required=True, write_only=True)
    is_login = serializers.SerializerMethodField(read_only=True)

    def get_is_login(self, obj):    # noqa
        return True if obj else False

    def create(self, validated_data):
        user = authenticate(**validated_data)
        if not user:
            raise serializers.ValidationError(detail='Invalid credential provided', code=status.HTTP_406_NOT_ACCEPTABLE)
        return user
