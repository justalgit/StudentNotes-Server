from rest_framework import serializers
from .models import User


class UserSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    name = serializers.CharField()
    surname = serializers.CharField()
    login = serializers.CharField()
    password = serializers.CharField()

    def create(self, validated_data):
        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.surname = validated_data.get("surname", instance.surname)
        instance.login = validated_data.get("login", instance.login)
        instance.password = validated_data.get("password", instance.password)
        instance.save()
        return instance
