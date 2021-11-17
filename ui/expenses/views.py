from django.shortcuts import render, redirect


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


def logout(request):
    return render(request, 'expenses/logout.html')


def admin(request):
    return redirect('http://0.0.0.0:8000/admin/')
