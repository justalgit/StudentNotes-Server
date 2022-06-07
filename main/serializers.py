from rest_framework import serializers
from .models import User, Group, Event, Request, UserGroupRelation


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


class UserNameSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    name = serializers.CharField()
    surname = serializers.CharField()

    def create(self, validated_data):
        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.surname = validated_data.get("surname", instance.surname)

        instance.save()

        return instance


class GroupSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    title = serializers.CharField()
    description = serializers.CharField(allow_null=True, allow_blank=True)
    last_modified_date = serializers.IntegerField()
    is_editable = serializers.BooleanField()
    is_private = serializers.BooleanField()
    creator_id = serializers.UUIDField()
    last_modified_user_id = serializers.UUIDField()

    def create(self, validated_data):
        return Group.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.description = validated_data.get("description", instance.description)
        instance.last_modified_date = validated_data.get("last_modified_date", instance.last_modified_date)
        instance.is_editable = validated_data.get("is_editable", instance.is_editable)
        instance.is_private = validated_data.get("is_private", instance.is_private)
        instance.creator_id = validated_data.get("creator_id", instance.creator_id)
        instance.last_modified_user_id = validated_data.get("last_modified_user_id", instance.last_modified_user_id)

        instance.save()

        return instance


class EventSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    title = serializers.CharField()
    description = serializers.CharField(allow_null=True, allow_blank=True)
    event_date = serializers.IntegerField()
    last_modified_date = serializers.IntegerField()
    is_editable = serializers.BooleanField()
    group_id = serializers.UUIDField()
    author_id = serializers.UUIDField()
    last_modified_user_id = serializers.UUIDField()

    def create(self, validated_data):
        return Event.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.description = validated_data.get("description", instance.description)
        instance.event_date = validated_data.get("event_date", instance.event_date)
        instance.last_modified_date = validated_data.get("last_modified_date", instance.last_modified_date)
        instance.is_editable = validated_data.get("is_editable", instance.is_editable)
        instance.group_id = validated_data.get("group_id", instance.group_id)
        instance.author_id = validated_data.get("author_id", instance.author_id)
        instance.last_modified_user_id = validated_data.get("last_modified_user_id", instance.last_modified_user_id)

        instance.save()

        return instance


class RequestSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    message = serializers.CharField(allow_null=True, allow_blank=True)
    request_date = serializers.IntegerField()
    author_id = serializers.UUIDField()
    group_id = serializers.UUIDField()

    def create(self, validated_data):
        return Request.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.message = validated_data.get("message", instance.message)
        instance.request_date = validated_data.get("request_date", instance.request_date)
        instance.author_id = validated_data.get("author_id", instance.author_id)
        instance.group_id = validated_data.get("group_id", instance.group_id)

        instance.save()

        return instance


class UserGroupRelationSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    user_id = serializers.UUIDField(read_only=True)
    group_id = serializers.UUIDField(read_only=True)

    def create(self, validated_data):
        return UserGroupRelation.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.user_id = validated_data.get("user_id", instance.user_id)
        instance.group_id = validated_data.get("group_id", instance.group_id)

        instance.save()

        return instance
