# Python
from typing import Any, Type

# Django
from django.db.models import QuerySet

# Rest
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.status import (
    HTTP_401_UNAUTHORIZED,
    HTTP_400_BAD_REQUEST,
    HTTP_200_OK,
    HTTP_404_NOT_FOUND
)

# Apps
from abstracts.mixins import (
    ResponseMixin,
)
from abstracts.paginators import AbstractPageNumberPaginator
from auths.serializers import CustomUserSerializer ,UserSerializer, UserProfileSerializer
from auths.models import CustomUser


class UserViewSet(
    ModelViewSet,
    RetrieveUpdateAPIView,
    ResponseMixin
):
    queryset: QuerySet[CustomUser] = CustomUser.objects.all()
    serializer_class = UserSerializer
    pagination_class: Type[AbstractPageNumberPaginator] = \
        AbstractPageNumberPaginator
    
    def list(self, request: Request) -> Response:

        paginator: AbstractPageNumberPaginator = \
            self.pagination_class()

        objects: list[Any] = paginator.paginate_queryset(
            self.queryset,
            request
        )
        serializer: UserSerializer = \
            UserSerializer(
                objects,
                many=True
            )
        return self.get_json_response(
            serializer.data,
            paginator
        )

    def create(self, request: Request):
        login = request.data['login']
        first_name = request.data['first_name']
        password = request.data['password']
        user = CustomUser.objects.create_user(
            login, first_name, password
        )
        return Response(data={
            'user id': f'id = {user.id}'
        }, status=201)
    
    
    @action(
        methods=['post'],
        url_path='get-token',
        detail=False,
    )
    def get_token(self, request: Request, *args, **kwargs):
        login = request.data['login']
        password = request.data['password']
        user: CustomUser = CustomUser.objects.filter(login=login).first()


        if user is None or not user.check_password(password):
            return Response(
                {
                    'error': 'Invalid credentials'
                }, 
                status=HTTP_401_UNAUTHORIZED
                )
            
        CustomUser.objects.set_code(user)
        refresh: RefreshToken = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })


    @action(
        methods=['get'],
        detail=False,
        url_path='get-me',
        permission_classes=(
            IsAuthenticated,
        )
    )
    def get_me(self, request: Request):
        user: CustomUser = request.user
        serializer: UserProfileSerializer = \
            UserProfileSerializer(
                self.queryset.get(id=user.id)
            )
        return Response(
            data={
                'user': serializer.data,
            },
            status=201
        )

    @action(
        methods=['post'],
        detail=False,
        url_path='set-bot-code'
    )
    def set_bot_code(self, request: Request, format=None):
        serializer = CustomUserSerializer(data=request.data)
        
        if serializer.is_valid():
            try:
                chat_id = serializer.validated_data['chat_id']
                bot_code = serializer.validated_data['bot_code']
                user: CustomUser = CustomUser.objects.get(bot_code=bot_code)
                if user.chat_id:
                    return Response({'error': 'Пользователь уже иницирован!'}, status=HTTP_400_BAD_REQUEST)
                CustomUser.objects.set_chat_id(user, chat_id)
                return Response(status=HTTP_200_OK)
            except CustomUser.DoesNotExist:
                return Response({'error': 'Пользователь не найден'}, status=HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


    