from datetime import datetime

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from chat.models import ChatMessage
from chat.serializers import ChatMessageSerializer


class TestTemplate(APITestCase):
    def _create_user(self):
        self.user = User.objects.create_user(username='user', password='password')

    def setUpExtra(self):
        pass

    def setUp(self):
        self._create_user()
        self.setUpExtra()


class ChatMessageTest(TestTemplate):
    def setUpExtra(self):
        self.message = ChatMessage.objects.create(sender=self.user, message='hello', pub_date=datetime.now())

    def test_get_message_list(self):
        response = self.client.get(reverse('chat:select_message'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['next'], None)
        self.assertEqual(response.data['previous'], None)


class ChatMessageCreateTest(TestTemplate):
    def setUpExtra(self):
        self.client.login(username='user', password='password')
        self.data = {'message': 'message'}

    def test_create_message(self):
        resp = self.client.post(reverse('chat:create_message'), data=self.data)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resp.data, self.data)


class ChatMessageUpdateTest(TestTemplate):
    def setUpExtra(self):
        self.client.login(username='user', password='password')
        self.message = ChatMessage.objects.create(sender=self.user, message='hello', pub_date=datetime.now())

    def test_update_message(self):
        data = {'message': 'message'}
        response = self.client.put(reverse('chat:update_message', kwargs={'pk': self.message.pk}),
                                   data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, data)


class ChatMessageDeleteTest(TestTemplate):
    def setUpExtra(self):
        self.client.login(username='user', password='password')
        self.message = ChatMessage.objects.create(sender=self.user, message='hello', pub_date=datetime.now())

    def test_delete_message(self):
        response = self.client.delete(reverse('chat:update_message', kwargs={'pk': self.message.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
