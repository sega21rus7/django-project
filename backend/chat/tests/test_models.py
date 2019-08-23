from datetime import datetime

from django.contrib.auth.models import User
from django.test import TestCase

from chat.models import ChatMessage


class TestBase(TestCase):
    def _create_user(self):
        self.user = User.objects.create_user(username='user', password='password')

    def setUpExtra(self):
        pass

    def setUp(self):
        self._create_user()
        self.setUpExtra()


class ChatMessageTest(TestBase):
    def setUpExtra(self):
        ChatMessage.objects.create(sender=self.user, message='message', pub_date=datetime.now())

    def test_message(self):
        message = ChatMessage.objects.get(message='message')
        self.assertEqual(message.sender.username, 'user')
