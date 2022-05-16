from django.contrib import admin
from django.urls import path
from main import views
from main.views import UserAPIView

urlpatterns = [
    path('admin', admin.site.urls),
    path('login', views.log_in),
    path('api/v1/users', UserAPIView.as_view()),
    path('api/v1/users/<str:id>', UserAPIView.as_view())
]
