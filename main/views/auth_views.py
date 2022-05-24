from rest_framework.response import Response
from rest_framework.views import APIView

from main.models import User


class LoginAPIView(APIView):

    def post(self, request):
        user_login = request.data["login"]
        user_password = request.data["password"]

        try:
            user = User.objects.get(login=user_login, password=user_password)
        except:
            return Response(
                status = 401,
                data = {
                    "id": None,
                    "name": None,
                    "surname": None
                }
            )

        return Response(
            status = 200,
            data = {
                "id": user.id,
                "name": user.name,
                "surname": user.surname
            }
        )
