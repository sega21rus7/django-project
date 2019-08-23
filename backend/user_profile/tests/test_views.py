from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class TestBase(APITestCase):
    def _create_user(self):
        self.user = User.objects.create_user(username='user', password='password')

    def setUpExtra(self):
        pass

    def setUp(self):
        self._create_user()
        self.setUpExtra()

    def tearDown(self):
        self.client.logout()


class UserSignOutViewTest(TestBase):
    def setUpExtra(self):
        self.client.login(username='user', password='password')

    def test_user_sign_out(self):
        response = self.client.get(reverse('user_profile:sign_out'))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)


class UserViewTest(TestBase):
    def test_get_users_list(self):
        response = self.client.get(reverse('user_profile:select_user'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)


class UserCreateViewTest(APITestCase):
    def setUp(self):
        self.data = {
            'username': 'user2',
            'email': 'user2@mail.ru',
            'password': 'password',
            'confirm_password': 'password'
        }
        self.empty_data = self.data.fromkeys(self.data, '')
        self.create_url = 'user_profile:create_user'

    def test_create(self):
        resp = self.client.post(reverse(self.create_url), data=self.data)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        self.assertTrue(User.objects.filter(username=self.data['username']).exists())

    def test_create_failed(self):
        # передаем пустые данные
        resp = self.client.post(reverse(self.create_url), data=self.empty_data)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertTrue('username' in resp.data)
        self.assertTrue('email' in resp.data)
        self.assertTrue('password' in resp.data)
        self.assertTrue('confirm_password' in resp.data)

        # передаем невалидные данные
        data = {
            'username': '1',
            'email': '1',
            'password': '1',
            'confirm_password': '1'
        }
        resp = self.client.post(reverse(self.create_url), data=data)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertTrue('username' in resp.data)
        self.assertTrue('email' in resp.data)
        self.assertTrue('password' in resp.data)
        self.assertTrue('confirm_password' in resp.data)


class UserLoginViewTest(TestBase):
    def setUpExtra(self):
        self.data = {
            'username': 'user',
            'password': 'password'
        }

    def test_user_login(self):
        resp = self.client.post(reverse('user_profile:login_user'), data=self.data)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)


class UserUpdateDeleteViewTest(TestBase):
    def test_update(self):
        data = {
            'username': 'new_username',
            'email': 'new_email@mail.ru',
            'password': 'new_password',
            'confirm_password': 'new_password',
        }
        response = self.client.put(reverse('user_profile:update_user', kwargs={'pk': self.user.pk}),
                                   data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete(self):
        response = self.client.delete(reverse('user_profile:update_user', kwargs={'pk': self.user.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
