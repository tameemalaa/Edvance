from django.contrib.auth import get_user_model
from rest_framework import serializers
from djoser.serializers import UserCreateSerializer as BaseUserSerializer

User = get_user_model()
class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'role' ,'last_name' , "gender", "phone", "birth_date" , "created_at")
        required_fields = ('email', 'username' , )
    def validate_username(self, value):
        if '@' in value:
            raise serializers.ValidationError("Username can't include '@'") #TODO : not working 
        return value

class CurrentUserSerializer(BaseUserSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name','role', 'last_name' , "gender", "phone", "birth_date" , "created_at")

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('phone', 'gender', 'birth_date', 'first_name', 'last_name')

