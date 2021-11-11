from django.contrib.auth.models import User
from rest_framework import serializers

from .models import UserExpenses


class ExpensesSerializer(serializers.ModelSerializer):
    """Serializer for expenses data"""
    user = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username')

    class Meta:
        model = UserExpenses
        fields = ('user', 'expenses', 'created', 'last_updated')


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email']
        )
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email')
