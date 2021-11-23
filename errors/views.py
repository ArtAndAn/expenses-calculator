from django.shortcuts import render


def forbidden(request):
    return render(request, 'errors/403.html')
