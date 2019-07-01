from django.db import models
from django.contrib.auth.models import User


class ChatMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(max_length=500)
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'message'
        verbose_name_plural = 'messages'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.message
