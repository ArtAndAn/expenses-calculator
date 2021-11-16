from . import views
from django.urls import path

app_name = 'expenses'

urlpatterns = [
    path('check', views.data_check, name='data_check'),
    path('user/<int:user_id>', views.SingleUserExpenses.as_view())
]
