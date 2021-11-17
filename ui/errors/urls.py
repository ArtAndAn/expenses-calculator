from django.urls import path

from . import views

app_name = 'errors'

urlpatterns = [
    path('403', views.forbidden, name='home'),
]
