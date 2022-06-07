from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from main.models import User
from main.serializers import UserSerializer


class UserAPIView(APIView):

    def get(self, request, *args, **kwargs):
        id = kwargs.get("id", None)
        if not id:
            users = User.objects.all()
            return Response(
                status=status.HTTP_200_OK,
                data={'users': UserSerializer(users, many=True).data}
            )

        try:
            instance = User.objects.get(id=id)
        except:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={"error": "User with id = {} does not exists".format(id)}
            )

        return Response(
            status=status.HTTP_200_OK,
            data={'user': UserSerializer(instance).data}
        )


    def put(self, request, *args, **kwargs):
        id = kwargs.get("id", None)
        if not id:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"error": "Method PUT not allowed"}
            )

        try:
            instance = User.objects.get(id=id)
        except:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={"error": "User with id = {} does not exists".format(id)}
            )

        serializer = UserSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            status=status.HTTP_200_OK,
            data={'user': serializer.data}
        )
