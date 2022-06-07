from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from main.models import UserGroupRelation, Group
from main.serializers import UserGroupRelationSerializer


class UserGroupRelationAPIView(APIView):

    def get(self, request, *args, **kwargs):
        id = kwargs.get("id", None)
        if not id:
            user_group_relations = UserGroupRelation.objects.all()
            return Response(
                status=status.HTTP_200_OK,
                data={'user_group_relations': UserGroupRelationSerializer(user_group_relations, many=True).data}
            )

        try:
            instance = UserGroupRelation.objects.get(id=id)
        except:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={"error": "User-group relation with id = {} does not exists".format(id)}
            )

        return Response(
            status=status.HTTP_200_OK,
            data={'user_group_relation': UserGroupRelationSerializer(instance).data}
        )


    def delete(self, request, *args, **kwargs):
        current_user_id = request.query_params.get("user_id", None)
        current_group_id = request.query_params.get("group_id", None)
        if not (current_user_id or current_group_id):
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"error": "Query parameters <user_id> and <group_id> required"}
            )

        try:
            instance = UserGroupRelation.objects.get(user_id=current_user_id, group_id=current_group_id)
        except:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={"error": "User-group relation with user_id = {} and group_id = {} does not exists"
                            .format(current_user_id, current_group_id)}
            )

        instance.delete()

        users_in_current_group_count = len(UserGroupRelation.objects.filter(group_id = current_group_id))
        group = Group.objects.get(id = current_group_id)

        if group.creator.id == current_user_id:
            new_creator_id = UserGroupRelation.objects.filter(user_id != current_user_id)[0]
            group.creator = Group.objects.get(creator__id = new_creator_id)

        if users_in_current_group_count == 0:
            Group.objects.get(id = instance.group_id).delete()

        return Response(
            status=status.HTTP_200_OK,
            data={'user_group_relation': UserGroupRelationSerializer(instance).data}
        )
