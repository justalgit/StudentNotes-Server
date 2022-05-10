from wsgiref.simple_server import WSGIRequestHandler
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def logIn(request):

    data = json.loads(request.body)
    user_login = data["login"]
    user_password = data["password"]
    print("Login request: login = {}, password = {}".format(user_login, user_password))
    is_logged_in = user_login.lower() == "anton" and user_password == "1"

    return JsonResponse(
        {
            'isLoggedIn' : is_logged_in
        }
    )