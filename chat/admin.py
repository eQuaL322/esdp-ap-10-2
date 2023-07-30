from django.contrib import admin

from chat.models import ChatMessage


class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'sender', 'recipient',  'message',)
    search_fields = ['message']
    list_filter = ('sender', 'timestamp')


admin.site.register(ChatMessage, ChatMessageAdmin)

