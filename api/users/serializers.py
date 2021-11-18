from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=50,
                                     validators=[UniqueValidator(queryset=User.objects.all(),
                                                                 message='This username already exists')])
    email = serializers.EmailField(max_length=100,
                                  validators=[UniqueValidator(queryset=User.objects.all(),
                                                              message='This email is already taken')])
    password = serializers.CharField(write_only=True, max_length=50, min_length=5)
    password_rep = serializers.CharField(write_only=True, max_length=50, min_length=5)
    agreement = serializers.CharField(required=True)

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email']
        )
        return user

    def validate(self, attrs):
        if attrs['agreement'] != 'true':
            raise serializers.ValidationError({'agreement': 'You have to read and accept agreement'})
        if attrs['password'] != attrs['password_rep']:
            raise serializers.ValidationError({'password_rep': 'Your passwords are not equal'})
        else:
            return attrs

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'password_rep', 'agreement')


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=50, required=True)
    password = serializers.CharField(max_length=50, required=True)
