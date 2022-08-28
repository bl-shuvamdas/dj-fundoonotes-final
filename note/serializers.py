from rest_framework import serializers

from user.models import User
from user.serializers import ResisterSerializer
from .models import Note


class NoteSerializer(serializers.ModelSerializer):
    user = ResisterSerializer(read_only=True)
    collaborator = ResisterSerializer(read_only=True, many=True)

    class Meta:
        model = Note
        fields = ('id', 'title', 'description', 'user', 'collaborator')

    def create(self, validated_data):
        if 'user' not in validated_data:
            validated_data['user'] = User.objects.first()
        return Note.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for k, v in validated_data.items():
            setattr(instance, k, v)
        instance.save()
        return instance
