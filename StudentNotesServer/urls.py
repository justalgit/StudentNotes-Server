from django.contrib import admin
from django.urls import path
from StudentNotesServer.main import views

urlpatterns = [
    path('admin', admin.site.urls),
    path('login', views.logIn)
]
