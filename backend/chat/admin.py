from django.contrib import admin

from .models import ChatMessage


class ChatAdmin(admin.ModelAdmin):
    list_display = ("sender", "message", "pub_date")


admin.site.register(ChatMessage, ChatAdmin)
