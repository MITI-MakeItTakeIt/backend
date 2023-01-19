from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


# Create your models here.
class UserManager(BaseUserManager):
    use_for_related_fields = True
    
    def create_user(self, email=None, nickname=None, password=None, **kwargs):
        if not email:
            raise ValueError('이메일은 필수 입력 사항입니다.')
        if not nickname:
            raise ValueError('사용자 닉네임은 필수 입력 사항입니다.')
        if not password:
            raise ValueError('비밀번호는 필수 입력 사항입니다.')
        user = self.model(email=self.normalize_email(email), nickname=nickname)
        user.set_password(password)
        user.save()
        return user
            
    def create_superuser(self, email=None, nickname=None, password=None, **kwargs):
        user = self.create_user(email=email, nickname=nickname, password=password, **kwargs)
        user.is_staff = True
        user.save()
        return user
    
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)


class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True, null=False)
    nickname = models.CharField(max_length=50, unique=True, null=False)
    is_staff = models.BooleanField(default=False)
    is_activated = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True)
    
    USERNAME_FIELD = 'email'
    
    objects = UserManager()