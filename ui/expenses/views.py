from django.shortcuts import render


def home(request):
    return render(request, 'expenses/home.html')


def user_expenses(request):
    return render(request, 'expenses/user_expenses.html')


def add_expenses(request):
    return render(request, 'expenses/add_expenses.html')


def login(request):
    return render(request, 'expenses/login.html')


def register(request):
    return render(request, 'expenses/register.html')
