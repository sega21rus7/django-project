from rest_framework import serializers

from user_profile.serializers import UserSerializer
from .models import ChatMessage


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
