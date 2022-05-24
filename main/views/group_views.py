from rest_framework.response import Response
from rest_framework.views import APIView
from main.models import Group, User, UserGroupRelation
from main.serializers import GroupSerializer
from main.utils.raw_query_utils import get_groups_for_user


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
        UserGroupRelation.objects.create(
            user_id = group_creator_id,
            group_id = serializer.data["id"]
        )

        return Response({'group': serializer.data})


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

        return Response({'group': serializer.data})


    def delete(self, request, *args, **kwargs):
        id = kwargs.get("id", None)
        if not id:
            return Response({"error": "Method DELETE not allowed"})

        try:
            instance = Group.objects.get(id=id)
        except:
            return Response({"error": "Group with id = {} does not exists".format(id)})

        instance.delete()

        return Response({'group': GroupSerializer(instance).data})


class CurrentUserGroupsAPIView(APIView):

    def get(self, request, *args, **kwargs):
        id = kwargs.get("id", None)
        if not id:
            return Response({'error': 'Parameter <user_id> must be provided'})

        try:
            user = User.objects.get(id=id)
            print(user.id)
        except:
            return Response({"error": "User with id = {} does not exists".format(id)})

        current_user_groups = get_groups_for_user(id)
        return Response({'groups': GroupSerializer(current_user_groups, many=True).data})
