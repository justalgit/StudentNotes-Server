from rest_framework.response import Response
from rest_framework.views import APIView
from main.models import UserGroupRelation, Group
from main.serializers import UserGroupRelationSerializer


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

    def delete(self, request, *args, **kwargs):
        user_id = request.query_params.get("user_id", None)
        group_id = request.query_params.get("group_id", None)
        if not (user_id or group_id):
            return Response({"error": "Query parameters <user_id> and <group_id> required"})

        try:
            instance = UserGroupRelation.objects.get(user_id=user_id, group_id=group_id)
        except:
            return Response({"error": "User-group relation with user_id = {} and group_id = {} does not exists"
                            .format(user_id, group_id)})

        print(instance.user, instance.group)
        instance.delete()
        users_in_current_group_count = len(UserGroupRelation.objects.filter(group_id = group_id))
        if users_in_current_group_count == 0:
            Group.objects.get(id = instance.group_id).delete()

        return Response({'user_group_relation': UserGroupRelationSerializer(instance).data})
