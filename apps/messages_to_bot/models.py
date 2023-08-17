# Django
from django.db.models import (
    TextField,
    ForeignKey,
    CASCADE,
    Manager
)

# Apps
from abstracts.models import AbstractsDateTime
from auths.models import CustomUser


class MessagesToBotManager(Manager):
    def messages_by_user(self, user_id):
        return self.filter(user_id=user_id)
    
    
class MessagesToBot(AbstractsDateTime):
    user = ForeignKey(to=CustomUser, on_delete=CASCADE)
    text_of_message = TextField()

    objects = MessagesToBotManager()

    class Meta:
        ordering = ('created_at',)
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    def __str__(self):
        return f"{self.user}: {self.text_of_message[:30]}"
