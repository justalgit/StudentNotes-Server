from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from main.models import Event, Group, User
from main.serializers import EventSerializer


class EventAPIView(APIView):

    def get(self, request, *args, **kwargs):
        id = kwargs.get("id", None)
        if not id:
            events = Event.objects.all()
            return Response(
                status=status.HTTP_200_OK,
                data={'events': EventSerializer(events, many=True).data}
            )

        try:
            instance = Event.objects.get(id=id)
        except:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={"error": "Event with id = {} does not exists".format(id)}
            )

        return Response(
            status=status.HTTP_200_OK,
            data={'event': EventSerializer(instance).data}
        )


    def post(self, request):
        event_group_id = request.data["group_id"]
        event_author_id = request.data["author_id"]
        event_last_modified_user_id = request.data["last_modified_user_id"]

        try:
            Group.objects.get(id=event_group_id)
            User.objects.get(id=event_author_id)
            User.objects.get(id=event_last_modified_user_id)
        except:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={"error": "User with id = {} or {} or Group with id = {} does not exists"
                            .format(event_author_id, event_last_modified_user_id, event_group_id)}
            )

        serializer = EventSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            status=status.HTTP_201_CREATED,
            data={'event': serializer.data}
        )


    def put(self, request, *args, **kwargs):
        id = kwargs.get("id", None)
        if not id:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"error": "Method PUT not allowed"}
            )

        try:
            instance = Event.objects.get(id=id)
        except:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={"error": "Event with id = {} does not exists".format(id)}
            )

        serializer = EventSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            status=status.HTTP_200_OK,
            data={'event': serializer.data}
        )


    def delete(self, request, *args, **kwargs):
        id = kwargs.get("id", None)
        if not id:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"error": "Method DELETE not allowed"}
            )

        try:
            instance = Event.objects.get(id=id)
        except:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={"error": "Event with id = {} does not exists".format(id)}
            )

        instance.delete()

        return Response(
            status=status.HTTP_200_OK,
            data={'event': EventSerializer(instance).data}
        )
