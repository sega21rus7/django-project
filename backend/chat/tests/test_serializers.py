from django.contrib.auth.models import User
from django.test import TestCase

from chat.models import ChatMessage
from chat.serializers import ChatMessageChangeSerializer, ChatMessageSerializer, \
    UserChangeSerializer, UserSerializer


class UserCreate(TestCase):
    def _create_user(self):
        self.user = User.objects.create_user(username='user', password='password')

    def setUp(self):
        self._create_user()


class ChatMessageChangeSerializerTest(UserCreate):
    def setUp(self):
        super().setUp()
        self.message = ChatMessage.objects.create(sender=self.user, message='hello')
        self.serializer = ChatMessageChangeSerializer(instance=self.message)

    def test_serializer_contains_expected_data(self):
        data = self.serializer.data
        self.assertEqual(data['message'], 'hello')
        self.assertEqual(len(data), 1)


class ChatMessageSerializerTest(UserCreate):
    def setUp(self):
        super().setUp()
        self.message = ChatMessage.objects.create(sender=self.user, message='hello')
        self.serializer = ChatMessageSerializer(instance=self.message)

    def test_serializer_contains_expected_data(self):
        data = self.serializer.data
        self.assertEqual(len(data), 4)
        self.assertEqual(len(data['sender']), 3)

        self.assertEqual(data['id'], 1)
        self.assertEqual(data['message'], 'hello')


class UserSerializerTest(UserCreate):
    def setUp(self):
        super().setUp()
        self.serializer = UserSerializer(instance=self.user)

    def test_user_contains_expected_data(self):
        data = self.serializer.data
        self.assertEqual(len(data), 3)
        self.assertEqual(data['id'], 1)
        self.assertEqual(data['username'], 'user')
        self.assertEqual(data['email'], '')


class UserChangeSerializerTest(UserCreate):
    def setUp(self):
        super().setUp()
        self.serializer = UserChangeSerializer(instance=self.user)

    def test_user_contains_expected_data(self):
        data = self.serializer.data
        self.assertEqual(len(data), 3)

        self.assertEqual(data['username'], 'user')
        self.assertEqual(data['email'], '')
        self.assertEqual(data['password'], self.user.password)

