# Django
from django.db.models import (
    CharField,
    BooleanField,
)
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
)
from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ValidationError

# Apps
from abstracts.validators import APIValidator
from abstracts.models import AbstractsDateTime
from auths.utils import generate_code

class CustomUserManager(
    BaseUserManager
):
    def create_user(
            self,
            login: str,
            first_name: str,
            password: str
        ) -> 'CustomUser':
        if not login:
            raise ValidationError('login required')
        try:
            user: 'CustomUser' = self.model(
                login=login,
                first_name=first_name,
                password=password
            )
            user.set_password(password)
            user.save(using=self._db)
            return user
        except:
            raise APIValidator(
                'Данный пользователь уже существует',
                'message',
                '400',
            )

    def create_superuser(
        self, login, first_name:str, password: str
    ) -> 'CustomUser':
        user: 'CustomUser' = self.model(
            is_staff=True,
            login=login,
            first_name=first_name,
            password=password
        )
        user.is_superuser: bool = True
        user.is_active: bool = True
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def set_code(self, user: 'CustomUser'):
        while True and not user.chat_id:
            code = generate_code()  
            stmt = self.filter(bot_code=code).exists()
            if not stmt:
                user.bot_code = code
                user.save()
                break

    def set_chat_id(self, user: 'CustomUser', chat_id):
        user.chat_id = chat_id
        user.save()
        


class CustomUser(
    AbstractBaseUser,
    PermissionsMixin,
    AbstractsDateTime
):
    login = CharField(
        'Логин',
        unique=True,
        max_length=100,
        null=False
    )
    first_name = CharField(
        'Имя',
        max_length=100,
    )
    bot_code = CharField(
        'Код для связи с телеграмм',
        max_length=10,
        unique=True,
        null=True
    )
    chat_id = CharField(
        'ID чата пользователя в телеграмме',
        max_length=100,
        unique=True,
        null=True
    )
    
    is_active: BooleanField = BooleanField(default=True)
    is_staff = BooleanField(default=False)
    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = ['first_name']
    objects = CustomUserManager()

    class Meta:
        ordering = (
            'created_at',
        )
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'