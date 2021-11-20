from . import views
from django.urls import path

app_name = 'expenses'

urlpatterns = [
    path('category', views.CategoryView.as_view()),
    path('expenses', views.ExpensesView.as_view()),
    path('expenses/image', views.GetExpensesImage.as_view()),
]
