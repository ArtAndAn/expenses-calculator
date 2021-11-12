from . import views
from django.urls import path

urlpatterns = [
    path('register', views.CreateUser.as_view(), name='register'),
]
