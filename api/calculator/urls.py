from django.urls import path

from . import views

app_name = 'expenses'

urlpatterns = [
    path('category', views.CategoryView.as_view()),
    path('expenses', views.ExpensesView.as_view()),
    path('roundimage', views.GetExpensesRoundImage.as_view()),
    path('barimage', views.GetExpensesBarImage.as_view()),
]
