from django.contrib.auth import get_user_model
from rest_framework import serializers
from djoser.serializers import UserCreateSerializer as BaseUserSerializer

User = get_user_model()
class UserSerializer(BaseUserSerializer):
    password = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta(BaseUserSerializer.Meta):
        model = User
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name' )
    def validate_username(self, value):
        if '@' in value:
            raise serializers.ValidationError("Username can't include '@'") #TODO : not working 
        return value

class CurrentUserSerializer(BaseUserSerializer):
    password = serializers.CharField(style={"input_type": "password"}, write_only=True)
    FIELDS_TO_UPDATE = ['username', 'email', 'first_name', 'last_name']
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name' , "gender", "phone", "birth_date" ,"created_at", "password")
        