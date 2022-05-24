import json
from rest_framework.response import Response
from rest_framework.views import APIView
from main.models import Request, Group, User
from main.serializers import RequestSerializer


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

        return Response({'request': serializer.data})


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

        return Response({'request': serializer.data})


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
            UserGroupRelation.objects.create(
                user_id=instance.incoming_user_id,
                group_id=instance.group_id
            )

        instance.delete()

        return Response({'request': RequestSerializer(instance).data})
