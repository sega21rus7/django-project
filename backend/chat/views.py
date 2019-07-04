from django.contrib.auth import logout, login
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic.base import View
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *


# region TemplateViews


class IndexView(View):
    def get(self, request):
        template = 'chat/index.html'
        return render(request, template)


# endregion

# region UserViews
class UserSignOutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('chat:index'), status=status.HTTP_200_OK)


class UserUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserChangeSerializer
    queryset = User.objects.all()


class UserListView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserCreateView(generics.CreateAPIView):
    serializer_class = UserChangeSerializer

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


# endregion

# region ChatMessageViews
class ChatMessageCreateView(generics.CreateAPIView):
    serializer_class = ChatMessageChangeSerializer


class ChatMessageListView(generics.ListAPIView):
    serializer_class = ChatMessageSerializer
    queryset = ChatMessage.objects.all()


class ChatMessageUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ChatMessageChangeSerializer
    queryset = ChatMessage.objects.all()

# endregion
