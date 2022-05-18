from django.contrib import admin
from django.urls import path
from main.views import log_in, UserAPIView, GroupAPIView, EventAPIView, RequestAPIView

urlpatterns = [
    path('admin', admin.site.urls),
    path('login', log_in),
    path('api/v1/users', UserAPIView.as_view()),
    path('api/v1/users/<str:id>', UserAPIView.as_view()),
    path('api/v1/groups', GroupAPIView.as_view()),
    path('api/v1/groups/<str:id>', GroupAPIView.as_view()),
    path('api/v1/events', EventAPIView.as_view()),
    path('api/v1/events/<str:id>', EventAPIView.as_view()),
    path('api/v1/requests', RequestAPIView.as_view()),
    path('api/v1/requests/<str:id>', RequestAPIView.as_view())
]
