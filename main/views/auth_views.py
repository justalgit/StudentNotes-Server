from rest_framework.response import Response
from rest_framework.views import APIView

from main.models import User, UserGroupRelation
from main.serializers import GroupSerializer, EventSerializer, RequestSerializer, UserGroupRelationSerializer, UserNameSerializer
from main.utils.raw_query_utils import get_groups_for_user, get_events_for_user, get_requests_for_user


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


class InitialDataAPIView(APIView):

    def get(self, request, *args, **kwargs):
        requested_user_id = kwargs.get("id", None)
        if not requested_user_id:
            return Response({"error": "Parameter <user_id> required"})

        try:
            User.objects.get(id=requested_user_id)
        except:
            return Response({"error": "User with id = {} does not exists".format(requested_user_id)})

        requested_user_groups_list = UserGroupRelation.objects \
            .filter(user_id=requested_user_id) \
            .values_list('group_id', flat=True)
        available_user_relations = UserGroupRelation.objects \
            .filter(group_id__in=requested_user_groups_list)
        available_users = User.objects.filter(id__in = available_user_relations.values_list('user_id', flat=True))
        user_groups = get_groups_for_user(requested_user_id)
        user_events = get_events_for_user(requested_user_id)
        user_requests = get_requests_for_user(requested_user_id)


        return Response(
            {
                "users": UserNameSerializer(available_users, many=True).data,
                "groups": GroupSerializer(user_groups, many=True).data,
                "events": EventSerializer(user_events, many=True).data,
                "requests": RequestSerializer(user_requests, many=True).data,
                "user_group_relations": UserGroupRelationSerializer(available_user_relations, many=True).data
            }
        )
