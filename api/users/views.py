from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import RegisterSerializer, LoginSerializer


class CreateUser(CreateAPIView):
    model = User
    serializer_class = RegisterSerializer


class LoginUser(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.data['username']
        password = serializer.data['password']

        user = authenticate(username=username, password=password)

        if user is None:
            pass  # TODO authorisation error

        login(request, user)
        return Response({'message': 'user logged in'})


class LogoutUser(APIView):
    def get(self, request):
        logout(request)
        return Response({'message': 'user logged out'})
