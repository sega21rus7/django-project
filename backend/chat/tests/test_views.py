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


class UserSignOutTest(APITestCase):
    def test_user_sign_in(self):
        response = self.client.get('/sign_out/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


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
        first_user = User.objects.create_user(username='first_user', email='first_user@mail.ru', password='password')
        second_user = User.objects.create_user(username='second_user', email='second_user@mail.ru', password='password')
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
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.data['results'], serializer.data)


class UserCreateTest(APITestCase):
    def test_create_user(self):
        post_data = {
            'username': 'mouse',
            'email': 'mouse@mail.ru',
            'password': 'password',
            'confirm_password': 'password'
        }
        get_data = {
            'username': 'mouse',
            'email': 'mouse@mail.ru'
        }
        response = self.client.post('/api/user/create/', post_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, get_data)


class UserLoginTest(APITestCase):
    def setUp(self):
        User.objects.create_user(username='lava172', email='', password='password')

    def test_user_login(self):
        post_data = {
            'username': 'lava172',
            'password': 'password'
        }
        get_data = {
            'username': 'lava172'
        }
        response = self.client.post('/api/user/login/', post_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, get_data)


class CreateChatMessageTest(APITestCase):
    def test_create_message(self):
        User.objects.create_user(username='sender', email='sender@mail.ru', password='password')
        self.client.login(username='sender', password='password')
        message = 'message'
        data = {
            'message': message
        }
        response = self.client.post('/api/chat_message/create/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, data)


class UpdateChatMessageTest(APITestCase):
    my_field = 1

    @classmethod
    def clsmthd(cls):
        cls.my_field = 2
        pass

    def setUp(self):
        self.my_field = 3
        self.sender = User.objects.create_user(username='sender', email='sender@mail.ru', password='password')
        self.client.login(username='sender', password='password')
        self.message = ChatMessage.objects.create(sender=self.sender, message='hello', pub_date=datetime.now())
        self.updated_message = 'hi'

    def test_update_message(self):
        data = {'message': self.updated_message}
        response = self.client.put('/api/chat_message/update/%d/' % self.message.id,  # kwargs={'pk': self.message.pk}
                                   data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data, data)
