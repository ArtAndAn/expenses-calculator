from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie, csrf_exempt
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import RegisterSerializer, LoginSerializer


@method_decorator(csrf_protect, name='dispatch')
class CreateUser(APIView):
    model = User
    serializer_class = RegisterSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid()
        if serializer.validated_data:
            serializer.create(serializer.validated_data)
            return Response(data={'message': 'registered'},
                            status=status.HTTP_201_CREATED)
        else:
            return Response(data={'message': 'error', 'errors': serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_protect, name='dispatch')
class LoginUser(APIView):
    serializer_class = LoginSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid()

        if not serializer.validated_data:
            return Response(data={'message': 'error', 'errors': serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)
        username = serializer.data['username']
        password = serializer.data['password']

        user = authenticate(username=username, password=password)

        if user is None:
            return Response(data={'message': 'error',
                                  'errors': {'password': 'There is no user with such username and password.'}})
        login(request, user)
        response = Response({'message': 'logged in'})
        response.set_cookie('sessionid', request.session.session_key)
        return response


class LogoutUser(APIView):
    def post(self, request):
        logout(request)
        return Response({'message': 'logged out'})


@method_decorator(csrf_protect, name='dispatch')
class UserData(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        user = request.user
        return Response({'message': 'user data',
                         'user': {'id': user.id,
                                  'username': user.username,
                                  'is_staff': user.is_staff,
                                  'is_authenticated': user.is_authenticated,
                                  'is_superuser': user.is_superuser
                                  }
                         })


@method_decorator(ensure_csrf_cookie, name='dispatch')
class GetCSRFToken(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        return Response({'success': 'CSRF cookie set'})
