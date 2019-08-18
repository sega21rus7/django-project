from datetime import datetime

from django.contrib.auth.models import User
from django.test import TestCase

from chat.models import ChatMessage


class ChatMessageTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='user', email='user@mail.ru', password='')
        ChatMessage.objects.create(sender=user, message='hi guys', pub_date=datetime.now())

    def test_message(self):
        message = ChatMessage.objects.get(message='hi guys')
        self.assertEqual(message.sender.username, 'user')
