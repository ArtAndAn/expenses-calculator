from django.contrib.auth.models import User
from django.shortcuts import redirect
from rest_framework.generics import RetrieveUpdateAPIView

from .models import Category, UserExpenses
from .serializers import ExpensesSerializer


class SingleUserExpenses(RetrieveUpdateAPIView):
    """View for showing single article data (only GET method)"""
    queryset = UserExpenses.objects.all()
    serializer_class = ExpensesSerializer
    lookup_field = 'user_id'


def data_check(request):
    categories = Category.objects.all()
    users = User.objects.all()

    if not categories:
        cat_list = ['Photography', 'Investigations', 'Tech', 'World', 'Sports', 'Arts', 'Entertainment', 'Business',
                    'Climate', 'Environment', 'Education', 'Food', 'Health', 'History', 'Lifestyle', 'Media', 'Science',
                    'Weather', 'Magazine', 'Opinions']
        Category.objects.bulk_create([Category(name=category) for category in cat_list])

    if len(users) <= 1:
        user_list = [
            {'name': 'irritabledirector', 'password': 'Wt}4t@X@~S2=/+pC'},
            {'name': 'starchyotter', 'password': 'M*43Hwkbk<YTqQ/@'},
            {'name': 'wombposse', 'password': 'k@_KHwmkSh7$d9wZ'},
            {'name': 'fireworkbeloved', 'password': '4Cwbbws</S2!3sb]'},
            {'name': 'cornettotrustee', 'password': 'csP<+7S!Ef97C'},
            {'name': 'choirbeloved', 'password': 'L{,+.w8wmQH]>e/a'},
            {'name': 'unsungduct', 'password': 'pV=E/ZhEd84?b";@'},
            {'name': 'fumerebel', 'password': 'Vs!$~MW8/%mX]8X%'},
            {'name': 'affectmalaysian', 'password': 'Zwq5;&SR9LWJSjc<'},
            {'name': 'fizzmojang', 'password': '<5Fg%Nyadh}X5:mc'}
        ]
        for user in user_list:
            User.objects.create_user(username=user['name'], password=user['password'])

    UserExpenses(user=request.user,
                 category=Category.objects.get(name='Investigations'),
                 spend=5436
                 ).save()

    UserExpenses(user=request.user,
                 category=Category.objects.get(name='Education'),
                 spend=6543252
                 ).save()

    UserExpenses(user=request.user,
                 category=Category.objects.get(name='Environment'),
                 spend=65423234
                 ).save()

    UserExpenses(user=request.user,
                 category=Category.objects.get(name='Food'),
                 spend=321431
                 ).save()

    return redirect('/')
