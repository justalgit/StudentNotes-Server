import distutils
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User, Group, Event, Request, UserGroupRelation
from .serializers import UserSerializer, GroupSerializer, EventSerializer, RequestSerializer, \
    UserGroupRelationSerializer


class UserAPIView(APIView):

    def get(self, request, *args, **kwargs):
        id = kwargs.get("id", None)
        if not id:
            users = User.objects.all()
            return Response({'users': UserSerializer(users, many=True).data})

        try:
            instance = User.objects.get(id=id)
        except:
            return Response({"error": "User with id = {} does not exists".format(id)})

        return Response({'user': UserSerializer(instance).data})


    def put(self, request, *args, **kwargs):
        id = kwargs.get("id", None)
        if not id:
            return Response({"error": "Method PUT not allowed"})

        try:
            instance = User.objects.get(id=id)
        except:
            return Response({"error": "User with id = {} does not exists".format(id)})

        serializer = UserSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'updated_user': serializer.data})

class GroupAPIView(APIView):

    def get(self, request, *args, **kwargs):
        id = kwargs.get("id", None)
        if not id:
            groups = Group.objects.all()
            return Response({'groups': GroupSerializer(groups, many=True).data})

        try:
            instance = Group.objects.get(id=id)
        except:
            return Response({"error": "Group with id = {} does not exists".format(id)})

        return Response({'group': GroupSerializer(instance).data})


    def post(self, request):
        group_creator_id = request.data["creator_id"]
        group_last_modified_user_id = request.data["last_modified_user_id"]
        try:
            User.objects.get(id=group_creator_id)
            User.objects.get(id=group_last_modified_user_id)
        except:
            return Response({"error": "User with id = {} or {} does not exists"
                            .format(group_creator_id, group_last_modified_user_id)})

        serializer = GroupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'created_group': serializer.data})


    def put(self, request, *args, **kwargs):
        id = kwargs.get("id", None)
        if not id:
            return Response({"error": "Method PUT not allowed"})

        try:
            instance = Group.objects.get(id=id)
        except:
            return Response({"error": "Group with id = {} does not exists".format(id)})

        serializer = GroupSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'updated_group': serializer.data})


    def delete(self, request, *args, **kwargs):
        id = kwargs.get("id", None)
        if not id:
            return Response({"error": "Method DELETE not allowed"})

        try:
            instance = Group.objects.get(id=id)
        except:
            return Response({"error": "Group with id = {} does not exists".format(id)})

        instance.delete()

        return Response({'deleted_group': GroupSerializer(instance).data})


class EventAPIView(APIView):

    def get(self, request, *args, **kwargs):
        id = kwargs.get("id", None)
        if not id:
            events = Event.objects.all()
            return Response({'events': EventSerializer(events, many=True).data})

        try:
            instance = Event.objects.get(id=id)
        except:
            return Response({"error": "Event with id = {} does not exists".format(id)})

        return Response({'event': EventSerializer(instance).data})


    def post(self, request):
        event_group_id = request.data["group_id"]
        event_author_id = request.data["author_id"]
        event_last_modified_user_id = request.data["last_modified_user_id"]

        try:
            Group.objects.get(id=event_group_id)
            User.objects.get(id=event_author_id)
            User.objects.get(id=event_last_modified_user_id)
        except:
            return Response({"error": "User with id = {} or {} or Group with id = {} does not exists"
                            .format(event_author_id, event_last_modified_user_id, event_group_id)})

        serializer = EventSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'created_event': serializer.data})


    def put(self, request, *args, **kwargs):
        id = kwargs.get("id", None)
        if not id:
            return Response({"error": "Method PUT not allowed"})

        try:
            instance = Event.objects.get(id=id)
        except:
            return Response({"error": "Event with id = {} does not exists".format(id)})

        serializer = EventSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'updated_event': serializer.data})


    def delete(self, request, *args, **kwargs):
        id = kwargs.get("id", None)
        if not id:
            return Response({"error": "Method DELETE not allowed"})

        try:
            instance = Event.objects.get(id=id)
        except:
            return Response({"error": "Event with id = {} does not exists".format(id)})

        instance.delete()

        return Response({'deleted_event': EventSerializer(instance).data})


class RequestAPIView(APIView):

    def get(self, request, *args, **kwargs):
        id = kwargs.get("id", None)
        if not id:
            requests = Request.objects.all()
            return Response({'requests': RequestSerializer(requests, many=True).data})

        try:
            instance = Request.objects.get(id=id)
        except:
            return Response({"error": "Request with id = {} does not exists".format(id)})

        return Response({'request': RequestSerializer(instance).data})


    def post(self, request):
        request_group_id = request.data["group_id"]
        request_author_id = request.data["author_id"]
        request_incoming_user_id = request.data["incoming_user_id"]

        try:
            Group.objects.get(id=request_group_id)
            User.objects.get(id=request_author_id)
            User.objects.get(id=request_incoming_user_id)
        except:
            return Response({"error": "User with id = {} or {} or Group with id = {} does not exists"
                            .format(request_author_id, request_incoming_user_id, request_group_id)})

        serializer = RequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'created_request': serializer.data})


    def put(self, request, *args, **kwargs):
        id = kwargs.get("id", None)
        if not id:
            return Response({"error": "Method PUT not allowed"})

        try:
            instance = Request.objects.get(id=id)
        except:
            return Response({"error": "Request with id = {} does not exists".format(id)})

        serializer = RequestSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'updated_request': serializer.data})


    def delete(self, request, *args, **kwargs):
        id = kwargs.get("id", None)
        is_accept = request.query_params.get("is_accept", None)
        if not id:
            return Response({"error": "Method DELETE not allowed"})
        if not is_accept:
            return Response({"error": "Method DELETE for request requires <is_accept> parameter"})

        try:
            instance = Request.objects.get(id=id)
        except:
            return Response({"error": "Request with id = {} does not exists".format(id)})

        if json.loads(is_accept):
            new_ugr = UserGroupRelation.objects.create(
                user_id=instance.incoming_user_id,
                group_id=instance.group_id
            )

        instance.delete()

        return Response({'deleted_request': RequestSerializer(instance).data})


class UserGroupRelationAPIView(APIView):

    def get(self, request, *args, **kwargs):
        id = kwargs.get("id", None)
        if not id:
            user_group_relations = UserGroupRelation.objects.all()
            return Response({'user_group_relations': UserGroupRelationSerializer(user_group_relations, many=True).data})

        try:
            instance = UserGroupRelation.objects.get(id=id)
        except:
            return Response({"error": "User-group relation with id = {} does not exists".format(id)})

        return Response({'user_group_relation': UserGroupRelationSerializer(instance).data})


@csrf_exempt
def log_in(request):
    data = json.loads(request.body)
    user_login = data["login"]
    user_password = data["password"]

    user = User.objects.filter(login=user_login, password=user_password)

    return JsonResponse({'isLoggedIn': len(user) == 1})
