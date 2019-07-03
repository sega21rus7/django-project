from datetime import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase

from chat.models import ChatMessage
from chat.serializers import ChatMessageListSerializer, UserListSerializer


class GetMainPageTemplateTest(TestCase):
    def test_main_page_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'chat/index.html')


class GetAllUsersTest(APITestCase):
    def setUp(self):
        for i in range(10):  # creating 10 users
            User.objects.create_user(username='user %s' % i)

    def test_get_users_list(self):
        response = self.client.get('/api/user/select/')
        user_list = User.objects.all()
        serializer = UserListSerializer(user_list, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 10)
        self.assertEqual(response.data['next'], None)
        self.assertEqual(response.data['previous'], None)
        self.assertEqual(response.data['results'], serializer.data)


class GetAllChatMessagesTest(APITestCase):
    def setUp(self):
        first_user = User.objects.create_user(username='first_user', email='first_user@mail.ru', password='')
        second_user = User.objects.create_user(username='second_user', email='second_user@mail.ru', password='')
        ChatMessage.objects.create(sender=first_user, message='hello', pub_date=datetime.now())
        ChatMessage.objects.create(sender=second_user, message='hi', pub_date=datetime.now())

    def test_get_message_list(self):
        response = self.client.get('/api/chat_message/select/')
        message_list = ChatMessage.objects.all()
        serializer = ChatMessageListSerializer(message_list, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
        self.assertEqual(response.data['next'], None)
        self.assertEqual(response.data['previous'], None)
        self.assertEqual(response.data['results'], serializer.data)


class CreateChatMessageTest(APITestCase):
    def test_create_message(self):
        User.objects.create_user(username='sender', email='sender@mail.ru', password='')
        self.client.login(username='sender', password='')
        message = 'message'
        data = {
            'message': message
        }
        response = self.client.post('/api/chat_message/create/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, data)

# class UpdateChatMessageTest(APITestCase):
