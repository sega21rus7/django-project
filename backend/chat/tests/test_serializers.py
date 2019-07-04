from django.contrib.auth.models import User
from django.test import TestCase

from chat.models import ChatMessage
from chat.serializers import ChatMessageChangeSerializer, ChatMessageSerializer, UserChangeSerializer, UserSerializer


# region ChatMessageSerializersTest


class ChatMessageChangeTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.message_attributes = {
            'message': 'hello guys'
        }
        cls.sender = cls.sender = User.objects.create_user(username='admin4', email='admin4@mail.ru',
                                                           password='password')
        cls.message = ChatMessage.objects.create(sender=cls.sender, message=cls.message_attributes['message'])
        cls.serializer = ChatMessageChangeSerializer(instance=cls.message)
        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def test_message_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(data.keys(), self.message_attributes.keys())
        self.assertEqual(len(data), len(self.message_attributes))

    def test_fields_content(self):
        data = self.serializer.data
        self.assertEqual(data['message'], self.message_attributes['message'])


class ChatMessageListGetTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.message_attributes = {
            'id': 1,
            'sender': {
                'id': 1,
                'username': 'admin3',
                'email': 'admin3@mail.ru'
            },
            'message': 'hello',
            'pub_date': ''
        }
        cls.sender = User.objects.create_user(username=cls.message_attributes['sender']['username'],
                                              email=cls.message_attributes['sender']['email'], password='server')
        cls.message = ChatMessage.objects.create(sender=cls.sender, message=cls.message_attributes['message'])
        cls.serializer = ChatMessageSerializer(instance=cls.message)
        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def test_message_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(data.keys(), self.message_attributes.keys())
        self.assertEqual(len(data), 4)
        self.assertEqual(len(data['sender']), 3)

    def test_fields_content(self):
        data = self.serializer.data

        self.assertEqual(data['message'], self.message_attributes['message'])
        # self.assertEqual(data['id'], self.message_attributes['id'])
        # + pub_date
        # self.assertEqual(data['sender']['id'], self.message_attributes['sender']['id'])
        self.assertEqual(data['sender']['username'], self.message_attributes['sender']['username'])
        self.assertEqual(data['sender']['email'], self.message_attributes['sender']['email'])


# endregion


# region UserSerializersTest


class UserListGetTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user_attributes = {
            'id': 1,
            'username': 'admin2',
            'email': 'admin@mail.ru'
        }
        cls.user = User.objects.create_user(username=cls.user_attributes['username'],
                                            email=cls.user_attributes['email'], password='server')
        cls.serializer = UserSerializer(instance=cls.user)
        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def test_user_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(data.keys(), self.user_attributes.keys())
        self.assertEqual(len(data), 3)

    def test_fields_content(self):
        data = self.serializer.data

        self.assertEqual(data['username'], self.user_attributes['username'])
        self.assertEqual(data['email'], self.user_attributes['email'])


class UserChangeTest(TestCase):
    @classmethod
    def setUpClass(cls):
        # cls.plain_password = 'server'
        cls.user_attributes = {
            'username': 'admin',
            'email': 'admin@mail.ru',
            'password': 'server',
        }
        cls.user = User.objects.create_user(**cls.user_attributes)
        cls.serializer = UserChangeSerializer(instance=cls.user)
        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def test_user_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(data.keys(), self.user_attributes.keys())
        self.assertEqual(len(data), 3)

    def test_fields_content(self):
        data = self.serializer.data
        self.assertEqual(data['username'], self.user_attributes['username'])
        self.assertEqual(data['email'], self.user_attributes['email'])
        # self.assertEqual(data['password'], make_password(self.plain_password))

# endregion
