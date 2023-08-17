from rest_framework.serializers import (
    ModelSerializer
)
from messages_to_bot.models import MessagesToBot



class MessageSerializer(ModelSerializer):
    
    class Meta:
        model = MessagesToBot
        fields = [
            'text_of_message',
            'created_at'
        ]