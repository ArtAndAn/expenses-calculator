from . import views
from django.urls import path

app_name = 'expenses'

urlpatterns = [
    path('category', views.CategoryView.as_view()),
    path('expenses', views.ExpensesView.as_view()),
    path('expenses/roundimage', views.GetExpensesRoundImage.as_view()),
    path('expenses/barimage', views.GetExpensesBarImage.as_view()),
]
