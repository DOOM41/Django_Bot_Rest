from rest_framework.serializers import (
    ModelSerializer,
    CharField,
    Serializer
)
from auths.models import CustomUser


class CustomUserSerializer(Serializer):
    bot_code = CharField()
    chat_id = CharField()
    


class UserSerializer(ModelSerializer):
    
    class Meta:
        model = CustomUser
        fields = [
            'created_at',
            'login',
            'first_name',
            'password'
        ]
        
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
class UserProfileSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            'id', 
            'login', 
            'first_name', 
            'bot_code'
        )
        

class CustomUserSerializer(Serializer):
    bot_code = CharField()
    chat_id = CharField()