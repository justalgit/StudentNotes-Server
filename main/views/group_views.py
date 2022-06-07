from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from main.models import Group, User, UserGroupRelation
from main.serializers import GroupSerializer


class GroupAPIView(APIView):

    def get(self, request, *args, **kwargs):
        id = kwargs.get("id", None)
        if not id:
            groups = Group.objects.all()
            return Response(
                status=status.HTTP_200_OK,
                data={'groups': GroupSerializer(groups, many=True).data}
            )

        try:
            instance = Group.objects.get(id=id)
        except:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={"error": "Group with id = {} does not exists".format(id)}
            )

        return Response(
            status=status.HTTP_200_OK,
            data={'group': GroupSerializer(instance).data}
        )


    def post(self, request):
        group_creator_id = request.data["creator_id"]
        group_last_modified_user_id = request.data["last_modified_user_id"]
        try:
            User.objects.get(id=group_creator_id)
            User.objects.get(id=group_last_modified_user_id)
        except:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={"error": "User with id = {} or {} does not exists"
                            .format(group_creator_id, group_last_modified_user_id)}
            )

        serializer = GroupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        UserGroupRelation.objects.create(
            user_id = group_creator_id,
            group_id = serializer.data["id"]
        )
        return Response(
            status=status.HTTP_201_CREATED,
            data={'group': serializer.data}
        )


    def put(self, request, *args, **kwargs):
        id = kwargs.get("id", None)
        if not id:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"error": "Method PUT not allowed"}
            )

        try:
            instance = Group.objects.get(id=id)
        except:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={"error": "Group with id = {} does not exists".format(id)}
            )

        serializer = GroupSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            status=status.HTTP_200_OK,
            data={'group': serializer.data}
        )


    def delete(self, request, *args, **kwargs):
        id = kwargs.get("id", None)
        if not id:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"error": "Method DELETE not allowed"}
            )

        try:
            instance = Group.objects.get(id=id)
        except:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={"error": "Group with id = {} does not exists".format(id)}
            )

        instance.delete()

        return Response(
            status=status.HTTP_200_OK,
            data={'group': GroupSerializer(instance).data}
        )
