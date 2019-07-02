from datetime import datetime

from django.contrib.auth.models import User
from django.test import TestCase

from chat.models import ChatMessage


class ChatMessageTest(TestCase):
    def setUp(self):
        man = User.objects.create_user(username='man', email='man@mail.ru', password='')
        women = User.objects.create_user(username='woman', email='women@mail.ru', password='')

        ChatMessage.objects.create(sender=man, message='hi guys', pub_date=datetime.now())
        ChatMessage.objects.create(sender=women, message='hello', pub_date=datetime.now())

    def test_message(self):
        man_message = ChatMessage.objects.get(message='hi guys')
        women_message = ChatMessage.objects.get(message='hello')
        self.assertEqual(man_message.sender.username, 'man')
        self.assertEqual(women_message.sender.username, 'woman')
