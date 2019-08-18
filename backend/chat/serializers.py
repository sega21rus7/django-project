from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import ChatMessage


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')

    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if not user:
            raise serializers.ValidationError('There was typing wrong login or password')
        return data


class UserChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'confirm_password')

    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        min_length=5,
        max_length=32,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(min_length=6, style={'input_type': 'password'})
    confirm_password = serializers.CharField(min_length=6, write_only=True, style={'input_type': 'password'})

    def validate(self, data):
        if data['password'] != data.pop('confirm_password'):
            raise serializers.ValidationError("Passwords do not match!")
        return data

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'],
                                        validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.set_password(self.validated_data['password'])
        instance.save()
        return instance


class ChatMessageChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ('message', 'sender')

    sender = serializers.HiddenField(default=serializers.CurrentUserDefault())


class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ('id', 'sender', 'message', 'pub_date')

    sender = UserSerializer()
    pub_date = serializers.DateTimeField('%d-%m-%y at %H:%M:%S')
