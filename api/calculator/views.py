import datetime

from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .draw_charts import draw_pie_chart, draw_column_chart
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

    # def get_queryset(self):
    #     time_period = self.request.GET.get('period', '')
    #     queryset = get_period_queryset(user=self.request.user, time_period=time_period)
    #     if not queryset['message']:
    #         for element in queryset:  # TODO write test if queryset has ErrorResponse or expenses
    #             element.date = element.date.strftime("%-d %B %Y")
    #     return queryset

    def list(self, request, *args, **kwargs):
        time_period = self.request.GET.get('period', '')
        if ':' in time_period:
            dates = time_period.split(':')
            if not dates[0] or not dates[1]:
                return Response(data={'message': 'error',
                                      'error': 'Check that both dates are filled'},
                                status=status.HTTP_400_BAD_REQUEST)
            from_date = datetime.datetime.strptime(dates[0], '%Y-%m-%d')
            till_date = datetime.datetime.strptime(dates[1], '%Y-%m-%d')
            if till_date < from_date:
                return Response(data={'message': 'error',
                                      'error': 'Check that "From" date is less than "Till" date'},
                                status=status.HTTP_400_BAD_REQUEST)
            queryset = get_period_queryset(self.request.user, time_period, from_date, till_date)
        else:
            queryset = get_period_queryset(self.request.user, time_period)
        serializer = self.get_serializer(queryset, many=True)
        return Response(data={'message': 'ok', 'data': serializer.data}, status=status.HTTP_200_OK)


def get_period_queryset(user, time_period, from_date=None, till_date=None):
    today = datetime.date.today()
    if time_period == 'total':
        queryset = UserExpenses.objects.filter(user=user).order_by('-date')[:10]
    elif time_period == 'month':
        queryset = UserExpenses.objects.filter(user=user).filter(date__month=today.month).order_by(
            '-date')[:10]
    elif time_period == 'week':
        queryset = UserExpenses.objects.filter(user=user).filter(
            date__range=[today - datetime.timedelta(days=7), today]).order_by('-date')[:10]
    else:
        queryset = UserExpenses.objects.filter(user=user).filter(
            date__range=[from_date, till_date]).order_by('-date')[:10]
    return queryset


class GetExpensesRoundImage(APIView):
    def get(self, request):
        time_period = self.request.GET.get('period', '')
        if ':' in time_period:
            dates = time_period.split(':')
            if not dates[0] or not dates[1]:
                return Response(data={'message': 'error',
                                      'error': 'Check that both dates are filled'},
                                status=status.HTTP_400_BAD_REQUEST)
            from_date = datetime.datetime.strptime(dates[0], '%Y-%m-%d')
            till_date = datetime.datetime.strptime(dates[1], '%Y-%m-%d')
            if till_date < from_date:
                return Response(data={'message': 'error',
                                      'error': 'Check that "From" date is less than "Till" date'},
                                status=status.HTTP_400_BAD_REQUEST)
            queryset = get_period_queryset(self.request.user, time_period, from_date, till_date)
        else:
            queryset = get_period_queryset(self.request.user, time_period)
        chart = draw_pie_chart(queryset)
        return HttpResponse(chart, content_type="image/png")


class GetExpensesBarImage(APIView):
    def get(self, request):
        time_period = self.request.GET.get('period', '')
        if ':' in time_period:
            dates = time_period.split(':')
            if not dates[0] or not dates[1]:
                return Response(data={'message': 'error',
                                      'error': 'Check that both dates are filled'},
                                status=status.HTTP_400_BAD_REQUEST)
            from_date = datetime.datetime.strptime(dates[0], '%Y-%m-%d')
            till_date = datetime.datetime.strptime(dates[1], '%Y-%m-%d')
            if till_date < from_date:
                return Response(data={'message': 'error',
                                      'error': 'Check that "From" date is less than "Till" date'},
                                status=status.HTTP_400_BAD_REQUEST)
            queryset = get_period_queryset(self.request.user, time_period, from_date, till_date)
        else:
            queryset = get_period_queryset(self.request.user, time_period)
        chart = draw_column_chart(queryset)
        return HttpResponse(chart, content_type="image/png")
