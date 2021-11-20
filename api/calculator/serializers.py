from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Category, UserExpenses


class CategoryRelatedField(serializers.SlugRelatedField):
    def get_queryset(self):
        queryset = Category.objects.all()
        request = self.context.get('request', None)
        queryset = queryset.filter(user=request.user)
        return queryset


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


class ExpensesSerializer(serializers.ModelSerializer):
    category = CategoryRelatedField(queryset=Category.objects.all(), slug_field='name', required=True)
    spend = serializers.FloatField(min_value=0, max_value=1000000, required=True)
    date = serializers.DateField(required=True)
    user = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username', required=True)

    class Meta:
        model = UserExpenses
        fields = ('category', 'spend', 'date', 'user')
