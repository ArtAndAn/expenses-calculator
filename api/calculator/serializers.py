from django.contrib.auth.models import User
from rest_framework import serializers

from .models import UserExpenses, Category


class ExpensesSerializer(serializers.ModelSerializer):
    """Serializer for expenses data"""
    user = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username')

    class Meta:
        model = UserExpenses
        fields = ('user', 'category', 'spend', 'date')


class CategorySerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username', required=True)
    name = serializers.CharField(max_length=50, required=True)

    def validate(self, attrs):
        if Category.objects.filter(user=attrs['user']).filter(name=attrs['name']):
            raise serializers.ValidationError({attrs['name']: 'You already have this category.'})
        else:
            return attrs

    class Meta:
        model = Category
        fields = ('name', 'user')
