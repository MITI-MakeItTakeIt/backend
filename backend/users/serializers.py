from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from utils.custom_fields import PasswordField
from utils.custom_validators import PasswordValidator


class UserBaseSerializer(serializers.ModelSerializer):
    password = PasswordField(required=True, write_only=True)
    password_check = PasswordField(required=True, write_only=True)
    
    class Meta:
        model = get_user_model()
        fields = ['email', 'nickname', 'password', 'password_check']
        
    def validate(self, data):
        if data['password'] != data['password_check']:
            raise serializers.ValidationError("비밀번호가 일치하지 않습니다.")
        return data
    
    def create(self, validated_data):
        user = self.Meta.model.objects.create_user(**validated_data)
        return user
    

class UserInfoCheckSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=False, validators=[UniqueValidator(queryset=get_user_model().objects.all())])
    nickname = serializers.CharField(
        required=False, validators=[UniqueValidator(queryset=get_user_model().objects.all())])
    
    _valid_fields = ('email', 'nickname')
    
    def validate(self, attrs):
        for field in self._valid_fields:
            if field in attrs:
                return {field: attrs[field]}
        raise serializers.ValidationError("email 혹은 nickname이 반드시 입력되어야 합니다.")    


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, write_only=True)
    password = serializers.CharField(required=True, write_only=True, validators=[PasswordValidator(),])
    
    def is_logginable(self, user):
        return user.is_loginnable_user()
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(email=email, password=password)
        
        if user is None:
            raise AuthenticationFailed("일치하는 회원 정보가 없습니다.")

        if self.is_logginable(user):
            attrs['user'] = user
            attrs['token'] = TokenObtainPairSerializer.get_token(user)
        
        return attrs
