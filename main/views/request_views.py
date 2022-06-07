import json

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from main.models import Request, Group, User, UserGroupRelation
from main.serializers import RequestSerializer, UserGroupRelationSerializer


class RequestAPIView(APIView):

    def get(self, request, *args, **kwargs):
        id = kwargs.get("id", None)
        if not id:
            requests = Request.objects.all()
            return Response(
                status=status.HTTP_200_OK,
                data={'requests': RequestSerializer(requests, many=True).data}
            )

        try:
            instance = Request.objects.get(id=id)
        except:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={"error": "Request with id = {} does not exists".format(id)}
            )

        return Response(
            status=status.HTTP_200_OK,
            data={'request': RequestSerializer(instance).data}
        )


    def post(self, request):
        request_group_id = request.data["group_id"]
        request_author_id = request.data["author_id"]

        try:
            request_group = Group.objects.get(id=request_group_id)
            request_author = User.objects.get(id=request_author_id)
        except:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={"error": "User with id = {} or Group with id = {} does not exists"
                            .format(request_author_id, request_group_id)}
            )

        if not request_group.is_private:
            ugr = UserGroupRelation(
                user_id = request_author_id,
                group_id = request_group_id
            )
            ugr.save()
            return Response(
                status=status.HTTP_201_CREATED,
                data={'user_group_relation': UserGroupRelationSerializer(ugr).data}
            )
        else:
            serializer = RequestSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                status=status.HTTP_201_CREATED,
                data={'request': serializer.data}
            )


    def put(self, request, *args, **kwargs):
        id = kwargs.get("id", None)
        if not id:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"error": "Method PUT not allowed"}
            )

        try:
            instance = Request.objects.get(id=id)
        except:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={"error": "Request with id = {} does not exists".format(id)}
            )

        serializer = RequestSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            status=status.HTTP_200_OK,
            data={'request': serializer.data}
        )


    def delete(self, request, *args, **kwargs):
        id = kwargs.get("id", None)
        is_accept = request.query_params.get("is_accept", None)
        if not id:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"error": "Method DELETE not allowed"}
            )
        if not is_accept:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"error": "Method DELETE for request requires <is_accept> parameter"}
            )

        try:
            instance = Request.objects.get(id=id)
        except:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={"error": "Request with id = {} does not exists".format(id)}
            )

        if json.loads(is_accept):
            UserGroupRelation.objects.create(
                user_id=instance.author_id,
                group_id=instance.group_id
            )

        instance.delete()

        return Response(
            status=status.HTTP_200_OK,
            data={'request': RequestSerializer(instance).data}
        )
