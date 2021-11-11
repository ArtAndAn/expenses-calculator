from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('charts', views.user_expenses, name='user_expenses'),
    path('add_expenses', views.add_expenses, name='add_expenses'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
]
