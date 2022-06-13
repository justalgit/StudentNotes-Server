from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from main.models import User, UserGroupRelation, Group, EventPriority
from main.serializers import GroupSerializer, EventSerializer, RequestSerializer, UserGroupRelationSerializer, UserNameSerializer
from main.utils.event_priority_utils import calculate_weighted_priority
from main.utils.raw_query_utils import get_events_for_user, get_requests_for_user


class LoginAPIView(APIView):

    def post(self, request):
        user_login = request.data["login"]
        user_password = request.data["password"]

        try:
            user = User.objects.get(login=user_login, password=user_password)
        except:
            return Response(status=status.HTTP_403_FORBIDDEN)

        return Response(
            status=status.HTTP_200_OK,
            data={
                "id": user.id,
                "name": user.name,
                "surname": user.surname
            }
        )


class InitialDataAPIView(APIView):

    def get(self, request, *args, **kwargs):
        requested_user_id = kwargs.get("id", None)
        if not requested_user_id:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"error": "Parameter <user_id> required"}
            )

        try:
            User.objects.get(id=requested_user_id)
        except:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={"error": "User with id = {} does not exists".format(requested_user_id)}
            )

        requested_user_groups_list = UserGroupRelation.objects \
            .filter(user_id=requested_user_id) \
            .values_list('group_id', flat=True)
        available_user_relations = UserGroupRelation.objects \
            .filter(group_id__in=requested_user_groups_list)
        available_users = User.objects.all()
        user_groups = Group.objects.all()
        user_events = get_events_for_user(requested_user_id)
        user_requests = get_requests_for_user(requested_user_id)
        for user_event in user_events:
            try:
                ep = EventPriority.objects.get(event_id = user_event.id, user_id = requested_user_id)
                user_event.weighted_priority = calculate_weighted_priority(
                    ep.user_priority,
                    ep.times_checked,
                    user_event.event_date
                )
                user_event.user_priority = ep.user_priority
            except:
                user_event.weighted_priority = calculate_weighted_priority(
                    user_event.user_priority,
                    0,
                    user_event.event_date
                )
            print(user_event.title, user_event.weighted_priority)

        return Response(
            status=status.HTTP_200_OK,
            data={
                "users": UserNameSerializer(available_users, many=True).data,
                "groups": GroupSerializer(user_groups, many=True).data,
                "events": EventSerializer(user_events, many=True).data,
                "requests": RequestSerializer(user_requests, many=True).data,
                "user_group_relations": UserGroupRelationSerializer(available_user_relations, many=True).data
            }
        )
