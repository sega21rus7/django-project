from datetime import datetime

from django.contrib.auth.models import User
from django.test import TestCase

from chat.models import ChatMessage


class UserCreate(TestCase):
    def _create_user(self):
        self.user = User.objects.create_user(username='user', password='password')

    def setUp(self):
        self._create_user()


class ChatMessageTest(UserCreate):
    def setUp(self):
        super().setUp()
        ChatMessage.objects.create(sender=self.user, message='hi guys', pub_date=datetime.now())

    def test_message(self):
        message = ChatMessage.objects.get(message='hi guys')
        self.assertEqual(message.sender.username, 'user')
