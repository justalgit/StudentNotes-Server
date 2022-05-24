from rest_framework.response import Response
from rest_framework.views import APIView
from main.models import User, Group, UserGroupRelation
from main.serializers import UserSerializer
from main.utils.raw_query_utils import get_users_for_group


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

        return Response({'user': serializer.data})


class CurrentGroupUsersAPIView(APIView):

    def get(self, request, *args, **kwargs):
        id = kwargs.get("id", None)
        if not id:
            return Response({'error': 'Query parameter <group_id> required'})

        try:
            Group.objects.get(id=id)
        except:
            return Response({"error": "Group with id = {} does not exists".format(id)})

        current_group_users = get_users_for_group(id)
        return Response({'groups': UserSerializer(current_group_users, many=True).data})
