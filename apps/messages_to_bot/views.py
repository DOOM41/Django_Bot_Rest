from typing import Any, Type
import asyncio

# Django
from django.db.models import QuerySet

# Rest
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request

# Apps
from abstracts.mixins import (
    ResponseMixin,
)
from abstracts.paginators import AbstractPageNumberPaginator
from messages_to_bot.serializers import MessageSerializer
from messages_to_bot.models import MessagesToBot
from messages_to_bot.utils import send_telegram_message
from auths.models import CustomUser

class MessageViewSet(
    ModelViewSet,
    RetrieveUpdateAPIView,
    ResponseMixin
):
    queryset: QuerySet[MessagesToBot] = MessagesToBot.objects.all()
    serializer_class = MessageSerializer
    pagination_class: Type[AbstractPageNumberPaginator] = \
        AbstractPageNumberPaginator
    permission_classes = (IsAuthenticated,)

    def create(self, request: Request):
        text = request.data['text_of_message']
        user: CustomUser = request.user
        if not user.chat_id:
            return Response(data={
                'result': "Вы не отправили код боту."
            }, status=400)
        mess = MessagesToBot.objects.create(
            user=user,
            text_of_message=text
        )
        mess.save()
        result_text = f"{user.first_name}, я получил от тебя сообщение:\n{text}"
        asyncio.run(send_telegram_message(
            chat_id=int(user.chat_id),
            text=result_text
        ))
        return Response(data={
            'result': "Sended"
        }, status=200)
    
    def list(self, request: Request) -> Response:

        paginator: AbstractPageNumberPaginator = \
            self.pagination_class()
        user: CustomUser = request.user
        objects: list[Any] = paginator.paginate_queryset(
            MessagesToBot.objects.messages_by_user(user),
            request
        )
        serializer: MessageSerializer = \
            MessageSerializer(
                objects,
                many=True
            )
        return self.get_json_response(
            serializer.data,
            paginator
        )