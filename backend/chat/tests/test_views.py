from datetime import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from chat.models import ChatMessage
from chat.serializers import ChatMessageSerializer, UserSerializer


# region TemplateTests
class MainPageTemplateGetTest(TestCase):
    def test_main_page_template(self):
        response = self.client.get(reverse('chat:index'))
        self.assertTemplateUsed(response, 'chat/index.html')


# endregion

# region UserViewsTests


class UserSignOutTest(APITestCase):
    def test_user_sign_in(self):
        response = self.client.get(reverse('chat:sign_out'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UserListGetTest(APITestCase):
    def setUp(self):
        for i in range(10):  # creating 10 users
            User.objects.create_user(username='user %s' % i)

    def test_get_users_list(self):
        response = self.client.get(reverse('chat:select_user'))
        user_list = User.objects.all()
        serializer = UserSerializer(user_list, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 10)
        self.assertEqual(response.data['next'], None)
        self.assertEqual(response.data['previous'], None)
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
        response = self.client.post(reverse('chat:create_user'), post_data)
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
        response = self.client.post(reverse('chat:login_user'), post_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, get_data)


class UserUpdateTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='lava172', email='', password='password')
        self.updated_username = 'lava573'
        self.updated_email = 'a@b.mail.ru'
        self.updated_password = 'new_password'

    def test_user_update_username(self):
        data = {
            'username': self.updated_username,
            'email': self.user.email,
            'password': self.user.password
        }
        response = self.client.put(reverse('chat:update_user', kwargs={'pk': self.user.pk}),
                                   data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, data)

    def test_user_update_password(self):
        data = {
            'username': self.user.username,
            'email': self.user.email,
            'password': self.updated_password
        }
        response = self.client.put(reverse('chat:update_user', kwargs={'pk': self.user.pk}),
                                   data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, data)

    def test_user_update_email(self):
        data = {
            'username': self.user.username,
            'email': self.updated_email,
            'password': self.user.password
        }
        response = self.client.put(reverse('chat:update_user', kwargs={'pk': self.user.pk}),
                                   data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, data)


class UserDeleteTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='lava172', email='', password='password')

    def test_delete_user(self):
        response = self.client.delete(reverse('chat:update_user', kwargs={'pk': self.user.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


# endregion

# region ChatMessageViewsTests


class ChatMessageListGetTest(APITestCase):
    def setUp(self):
        first_user = User.objects.create_user(username='first_user', email='first_user@mail.ru', password='password')
        second_user = User.objects.create_user(username='second_user', email='second_user@mail.ru', password='password')
        ChatMessage.objects.create(sender=first_user, message='hello', pub_date=datetime.now())
        ChatMessage.objects.create(sender=second_user, message='hi', pub_date=datetime.now())

    def test_get_message_list(self):
        response = self.client.get(reverse('chat:select_message'))
        message_list = ChatMessage.objects.all()
        serializer = ChatMessageSerializer(message_list, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
        self.assertEqual(response.data['next'], None)
        self.assertEqual(response.data['previous'], None)
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.data['results'], serializer.data)


class ChatMessageCreateTest(APITestCase):
    def test_create_message(self):
        User.objects.create_user(username='sender', email='sender@mail.ru', password='password')
        self.client.login(username='sender', password='password')
        message = 'message'
        data = {
            'message': message
        }
        response = self.client.post(reverse('chat:create_message'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, data)


class ChatMessageUpdateTest(APITestCase):
    # my_field = 1

    # @classmethod
    # def clsmthd(cls):
    #     cls.my_field = 2
    #     pass

    def setUp(self):
        # self.my_field = 3
        self.sender = User.objects.create_user(username='sender', email='sender@mail.ru', password='password')
        self.client.login(username='sender', password='password')
        self.message = ChatMessage.objects.create(sender=self.sender, message='hello', pub_date=datetime.now())
        self.updated_message = 'hi'

    def test_update_message(self):
        data = {'message': self.updated_message}
        response = self.client.put(reverse('chat:update_message', kwargs={'pk': self.message.pk}),
                                   data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, data)


class ChatMessageDeleteTest(APITestCase):
    def setUp(self):
        self.sender = User.objects.create_user(username='sender', email='sender@mail.ru', password='password')
        self.client.login(username='sender', password='password')
        self.message = ChatMessage.objects.create(sender=self.sender, message='hello', pub_date=datetime.now())

    def test_delete_message(self):
        response = self.client.delete(reverse('chat:update_message', kwargs={'pk': self.message.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

# endregion
