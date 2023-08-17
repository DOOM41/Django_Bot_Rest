from django.contrib import admin
from messages_to_bot.models import MessagesToBot

@admin.register(MessagesToBot)
class MessagesToBotAdmin(admin.ModelAdmin):
    list_display = ('user', 'text_of_message', 'created_at')
    list_filter = ('user', 'created_at')
    search_fields = ('user__login', 'text_of_message')
    date_hierarchy = 'created_at'
