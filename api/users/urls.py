from . import views
from django.urls import path

urlpatterns = [
    path('register', views.CreateUser.as_view(), name='register'),
    path('login', views.LoginUser.as_view(), name='login'),
    path('logout', views.LogoutUser.as_view(), name='logout'),
    path('user', views.UserData.as_view(), name='user_data'),
]
