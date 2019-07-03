from django.contrib.auth import logout, login, authenticate
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.base import View
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *


class IndexView(View):
    def get(self, request):
        template = 'chat/index.html'
        return render(request, template)


class UserSignOutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect("/", status=status.HTTP_200_OK)


class ChatMessageCreateView(generics.CreateAPIView):
    serializer_class = ChatMessageCreateSerializer


class ChatMessageListView(generics.ListAPIView):
    serializer_class = ChatMessageListSerializer
    queryset = ChatMessage.objects.all()


class ChatMessageUpdateView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ChatMessageCreateSerializer
    queryset = ChatMessage.objects.all()


class UserListView(generics.ListAPIView):
    serializer_class = UserListSerializer
    queryset = User.objects.all()


class UserCreateView(generics.CreateAPIView):
    serializer_class = UserCreateSerializer

    # def get(self, request):
    #     return Response(status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        if user:
            username = request.data.get('username')
            password = request.data.get('password')
            authenticate(username=username, password=password)
            login(request, user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    serializer_class = UserLoginSerializer

    # def get(self, request):
    #     return Response(status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            username = request.data.get('username')
            password = request.data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
