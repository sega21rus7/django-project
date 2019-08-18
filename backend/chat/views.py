from django.shortcuts import render
from django.views.generic.base import View
from rest_framework import generics

from .serializers import *


class IndexView(View):
    def get(self, request):
        template = 'chat/index.html'
        return render(request, template)


class ChatMessageCreateView(generics.CreateAPIView):
    serializer_class = ChatMessageChangeSerializer


class ChatMessageView(generics.ListAPIView):
    serializer_class = ChatMessageSerializer
    queryset = ChatMessage.objects.all()


class ChatMessageUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ChatMessageChangeSerializer
    queryset = ChatMessage.objects.all()
