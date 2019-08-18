from datetime import datetime

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from chat.models import ChatMessage
from chat.serializers import ChatMessageSerializer, UserSerializer


class UserCreate(APITestCase):
    def _create_user(self):
        self.user = User.objects.create_user(username='user', password='password')

    def setUp(self):
        self._create_user()


# исправить ошибку в самом функционале, стр. возвращает код 302
class UserSignOutViewTest(UserCreate):
    def setUp(self):
        super().setUp()
        self.client.login(username='user', password='password')

    def test_user_sign_out(self):
        response = self.client.get(reverse('chat:sign_out'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(self.user.is_authenticated)


class UserViewTest(UserCreate):
    def setUp(self):
        super().setUp()

    def test_get_users_list(self):
        response = self.client.get(reverse('user_profile:select_user'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['next'], None)
        self.assertEqual(response.data['previous'], None)


class UserCreateViewTest(APITestCase):
    def setUp(self):
        self.data = {
            'username': 'example',
            'email': 'example@mail.ru',
            'password': 'password',
            'confirm_password': 'password'
        }

    def test_create_user(self):
        resp = self.client.post(reverse('user_profile:create_user'), data=self.data)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        # доделать, исправить ошибку
        self.assertEqual(resp.data, self.data)


class UserLoginViewTest(UserCreate):
    def setUp(self):
        super().setUp()
        self.data = {
            'username': 'user',
            'password': 'password'
        }

    def test_user_login(self):
        resp = self.client.post(reverse('user_profile:login_user'), data=self.data)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue('user' in resp.data.values())


class UserUpdateDeleteViewTest(UserCreate):
    # изменить функционал, исправить ошибки
    def setUp(self):
        super().setUp()

    def test_user_data_update(self):
        data = {
            'username': 'new_username',
            'email': 'new_email@mail.ru',
            'password': 'new_password',
            'confirm_password': 'new_password',
        }
        response = self.client.put(reverse('user_profile:update_user', kwargs={'pk': self.user.pk}),
                                   data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, data)

    def test_delete_user(self):
        response = self.client.delete(reverse('user_profile:update_user', kwargs={'pk': self.user.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

