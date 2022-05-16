import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
from .serializers import UserSerializer


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

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'created_user': serializer.data})

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

    def delete(self, request, *args, **kwargs):
        id = kwargs.get("id", None)
        if not id:
            return Response({"error": "Method DELETE not allowed"})

        try:
            instance = User.objects.get(id=id)
        except:
            return Response({"error": "User with id = {} does not exists".format(id)})

        instance.delete()

        return Response({'deleted_user': UserSerializer(instance).data})


@csrf_exempt
def log_in(request):
    data = json.loads(request.body)
    user_login = data["login"]
    user_password = data["password"]
    print("Login request: login = {}, password = {}".format(user_login, user_password))

    user = User.objects.filter(login=user_login, password=user_password)
    print(user)
    is_logged_in = len(user) == 1

    return JsonResponse(
        {
            'isLoggedIn': is_logged_in
        }
    )
