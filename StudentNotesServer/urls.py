from django.contrib import admin
from django.urls import path
from main.views.auth_views import LoginAPIView, InitialDataAPIView
from main.views.event_views import EventAPIView
from main.views.group_views import GroupAPIView
from main.views.request_views import RequestAPIView
from main.views.user_group_relation_views import UserGroupRelationAPIView
from main.views.user_views import UserAPIView

urlpatterns = [
    path('admin', admin.site.urls),
    path('api/v1/login', LoginAPIView.as_view()),
    path('api/v1/initial-data/<str:id>', InitialDataAPIView.as_view()),
    path('api/v1/users', UserAPIView.as_view()),
    path('api/v1/users/<str:id>', UserAPIView.as_view()),
    path('api/v1/groups', GroupAPIView.as_view()),
    path('api/v1/groups/<str:id>', GroupAPIView.as_view()),
    path('api/v1/events', EventAPIView.as_view()),
    path('api/v1/events/<str:id>', EventAPIView.as_view()),
    path('api/v1/requests', RequestAPIView.as_view()),
    path('api/v1/requests/<str:id>', RequestAPIView.as_view()),
    path('api/v1/user-group-relations', UserGroupRelationAPIView.as_view()),
    path('api/v1/user-group-relations/<str:id>', UserGroupRelationAPIView.as_view())
]
