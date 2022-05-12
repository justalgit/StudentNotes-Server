from wsgiref.simple_server import WSGIRequestHandler
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from .models import User

@csrf_exempt
def logIn(request):

    data = json.loads(request.body)
    user_login = data["login"]
    user_password = data["password"]
    print("Login request: login = {}, password = {}".format(user_login, user_password))
    
    user = User.objects.filter(login = user_login, password = user_password)
    print(user)
    is_logged_in = len(user) == 1

    return JsonResponse(
        {
            'isLoggedIn' : is_logged_in
        }
    )