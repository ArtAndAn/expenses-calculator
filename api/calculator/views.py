from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .draw_charts import draw_charts
from .models import Category, UserExpenses
from .serializers import ExpensesSerializer, CategorySerializer


class CategoryView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def create(self, request, *args, **kwargs):
        user = User.objects.get(username=self.request.data[0]['user'])
        for category in self.request.data:
            category['user'] = user
        serializer = self.get_serializer(data=request.data, many=isinstance(request.data, list))
        serializer.is_valid()
        if serializer.validated_data:
            self.perform_create(serializer)
            return Response(data={'message': 'created'},
                            status=status.HTTP_201_CREATED)
        else:
            return Response(data={'message': 'error', 'errors': serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        default_user = User.objects.get(username='default')
        return Category.objects.filter(
            Q(user=self.request.user) | Q(user=default_user)).order_by('name')


class ExpensesView(ListCreateAPIView):
    queryset = UserExpenses.objects.all()
    serializer_class = ExpensesSerializer

    def create(self, request, *args, **kwargs):
        user = User.objects.get(username=self.request.data[0]['user'])
        for category in request.data:
            category['user'] = user
        serializer = self.get_serializer(data=request.data, many=isinstance(request.data, list))
        serializer.is_valid()
        if serializer.validated_data:
            self.perform_create(serializer)
            return Response(data={'message': 'created'},
                            status=status.HTTP_201_CREATED)
        else:
            return Response(data={'message': 'error', 'errors': serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        return UserExpenses.objects.filter(user=self.request.user).order_by('-date')


class GetExpensesImage(APIView):
    def get(self, request):
        expenses = UserExpenses.objects.filter(user=request.user).order_by('-date')
        chart = draw_charts(expenses)
        return HttpResponse(chart, content_type="image/png")
