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
    """
    View for creating new user categories and showing to client categories that he already has.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def create(self, request, *args, **kwargs):
        for category in self.request.data:
            category['user'] = request.user

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
    """
    View for creating new user expenses and showing to client expenses that he already has.
    """
    queryset = UserExpenses.objects.all()
    serializer_class = ExpensesSerializer

    def create(self, request, *args, **kwargs):
        for category in request.data:
            category['user'] = request.user

        serializer = self.get_serializer(data=request.data, many=isinstance(request.data, list))
        serializer.is_valid()

        if serializer.validated_data:
            self.perform_create(serializer)
            return Response(data={'message': 'created'},
                            status=status.HTTP_201_CREATED)
        else:
            return Response(data={'message': 'error', 'errors': serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        time_period = self.request.GET.get('period', '')

        queryset = get_time_period_queryset(time_period, request.user)
        if isinstance(queryset, str):
            return Response(data={'message': 'error', 'error': queryset}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(queryset, many=True)
        return Response(data={'message': 'ok', 'data': serializer.data}, status=status.HTTP_200_OK)


class GetExpensesRoundImage(APIView):
    """
    View for creating a round(pie) chart for selected time period user expenses
    """
    def get(self, request):
        time_period = self.request.GET.get('period', '')

        queryset = get_time_period_queryset(time_period, request.user)
        if isinstance(queryset, str):
            return Response(data={'message': 'error', 'error': queryset}, status=status.HTTP_400_BAD_REQUEST)

        chart = draw_pie_chart(queryset)
        return HttpResponse(chart, content_type="image/png")


class GetExpensesBarImage(APIView):
    """
    View for creating a bar(column) chart for selected time period user expenses
    """
    def get(self, request):
        time_period = self.request.GET.get('period', '')

        queryset = get_time_period_queryset(time_period, request.user)
        if isinstance(queryset, str):
            return Response(data={'message': 'error', 'error': queryset}, status=status.HTTP_400_BAD_REQUEST)

        chart = draw_column_chart(queryset)
        return HttpResponse(chart, content_type="image/png")


def get_time_period_queryset(time_period, user):
    """
    View that returns a user expenses queryset filtered by time period or error string if form data is not correct
    """
    if ':' in time_period:
        dates = time_period.split(':')
        if not dates[0] or not dates[1]:
            return 'Check that both dates are filled'
        from_date = datetime.datetime.strptime(dates[0], '%Y-%m-%d')
        till_date = datetime.datetime.strptime(dates[1], '%Y-%m-%d')
        if till_date < from_date:
            return 'Check that "From" date is less than "Till" date'
        queryset = return_queryset(user, time_period, from_date, till_date)
    else:
        queryset = return_queryset(user, time_period)
    return queryset


def return_queryset(user, time_period, from_date=None, till_date=None):
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
