from django.contrib.auth.models import User
from django.test import TestCase

from user_profile.serializers import UserSerializer, UserChangeSerializer


class TestBase(TestCase):
    def _create_user(self):
        self.user = User.objects.create_user(username='user', password='password')

    def setUpExtra(self):
        pass

    def setUp(self):
        self._create_user()
        self.setUpExtra()


class UserSerializerTest(TestBase):
    def setUpExtra(self):
        self.serializer = UserSerializer(instance=self.user)

    def test_user_contains_expected_data(self):
        data = self.serializer.data
        self.assertEqual(len(data), 3)
        self.assertEqual(data['id'], 1)
        self.assertEqual(data['username'], 'user')
        self.assertEqual(data['email'], '')


class UserChangeSerializerTest(TestBase):
    def setUpExtra(self):
        self.serializer = UserChangeSerializer(instance=self.user)

    def test_user_contains_expected_data(self):
        data = self.serializer.data
        self.assertEqual(len(data), 3)

        self.assertEqual(data['username'], 'user')
        self.assertEqual(data['email'], '')
        self.assertEqual(data['password'], self.user.password)
