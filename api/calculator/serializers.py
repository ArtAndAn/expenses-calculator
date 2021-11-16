from django.contrib.auth.models import User
from rest_framework import serializers

from .models import UserExpenses


class ExpensesSerializer(serializers.ModelSerializer):
    """Serializer for expenses data"""
    user = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username')

    class Meta:
        model = UserExpenses
        fields = ('user', 'category', 'spend', 'date')
