from rest_framework import serializers

from user.serializers import ResisterSerializer
from .models import Note


class NoteSerializer(serializers.ModelSerializer):
    collaborator = ResisterSerializer(read_only=True, many=True)

    class Meta:
        model = Note
        fields = ('id', 'title', 'description', 'user', 'collaborator')
        swagger_schema_fields = {"required": ['title', 'description']}

    def create(self, validated_data):
        return Note.objects.create(**validated_data)    # noqa

    def update(self, instance, validated_data):
        for k, v in validated_data.items():
            setattr(instance, k, v)
        instance.save()
        return instance


class CollaboratorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ('id', 'collaborator')
