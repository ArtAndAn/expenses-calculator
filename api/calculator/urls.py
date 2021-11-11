from . import views
from django.urls import path

app_name = 'expenses'

urlpatterns = [
    path('check', views.data_check, name='data_check'),
    path('register', views.CreateUser.as_view(), name='data_check'),
    # path('<int:user_id>', views.SingleUserExpenses.as_view(), name='user_expenses')
]
