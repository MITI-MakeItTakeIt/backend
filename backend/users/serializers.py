from django.contrib.auth import get_user_model
from rest_framework import serializers

from utils.custom_fields import PasswordField


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
    