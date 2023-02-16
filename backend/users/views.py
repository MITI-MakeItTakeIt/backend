from rest_framework import status, views
from rest_framework.response import Response
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError

from utils.user_activate_token_generator import user_activation_token
from utils.custom_emails import UserActivationEmail
from utils.custom_responses import UserInfoCheckResponse

from .serializers import *

import requests

# Create your views here.

class UserListView(views.APIView):
    
    def post(self, request):
        serializer = UserBaseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        uidb64 = urlsafe_base64_encode(force_bytes(user.id))
        token = user_activation_token.make_token(user)
        
        # TODO: 비동기 처리
        email = UserActivationEmail(uidb64, token, to=[user.email,])
        # email.send()
        return Response(
            serializer.data,
            status = status.HTTP_201_CREATED
        )
        
    
class UserActivateView(views.APIView):
    
    # TODO: request method 변경 예정
    def get(self, request, uidb64, token):
        try:
            uid = int(force_str(urlsafe_base64_decode(uidb64)))
        except DjangoUnicodeDecodeError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        user = get_user_model().objects.filter(pk=uid).first()

        # TODO: 발생 예외 정리 및 구현, 예외 처리
        if user is not None and user_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UserInfoCheckView(views.APIView):
    
    def get(self, request):
        check_field = request.GET.get('key', None)
        input_value = request.GET.get('value', None)
        
        response_data = UserInfoCheckResponse({check_field: input_value})
        response_data.is_valid()
        
        return Response(
            response_data.response,
            status = status.HTTP_200_OK
        )


class UserLoginView(views.APIView):
    
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            serializer.data,
            status = status.HTTP_200_OK
        )


class SocialLoginView(views.APIView):
    valid_social = ('kakao',)
    
    client_id = getattr(settings, 'KAKAO_REST_API_KEY')
    urls = getattr(settings, 'MITI_URLS')
    authorize_url = urls['KAKAO']['AUTHORIZE']
    redirect_uri = urls['CALLBACK']['KAKAO']['LOGIN_REDIRECT_URI']
            
    def get(self, request):
        social_service = request.GET.get('provider', None)
        
        if social_service not in self.valid_social:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        return Response(
            data = {'login_url': self.authorize_url%(self.client_id, self.redirect_uri)},
            status = status.HTTP_200_OK
        )
        
        
class LoginCallbackView(views.APIView):
    urls = getattr(settings, 'MITI_URLS')
    redirect_uri = urls['CALLBACK']['KAKAO']['LOGIN_REDIRECT_URI']
    content_type = 'application/x-www-form-urlencoded;charset=utf-8'
    kakao_usertoken_url = "https://kauth.kakao.com/oauth/token"
    kakao_userinfo_url = "https://kapi.kakao.com/v2/user/me"
    
    def get(self, request):
        authorize_code = request.GET.get('code', None)
                
        if authorize_code is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        data = {
            'grant_type': 'authorization_code',
            'client_id': getattr(settings, 'KAKAO_REST_API_KEY'),
            'redirect_uri': self.redirect_uri,
            'code': authorize_code
        }
        headers = {
            'Content-type': self.content_type
        }
        
        response = requests.post(self.kakao_usertoken_url, data=data, headers=headers)
        jsonified_response = response.json()

        HEADER = {
            'Authorization': "Bearer %s"%jsonified_response['access_token'],
            'Content-type': self.content_type
        }
        res = requests.get(self.kakao_userinfo_url, headers=HEADER).json()
        user_email = res['kakao_account']['email']
        nickname = res['properties']['nickname']

        user = get_user_model().objects.filter(email=user_email).first()
        
        if user is not None:
            serializer = UserLoginSerializer(user)
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        user = get_user_model().objects.create_social_user(email=user_email, nickname=nickname)
        serializer = UserLoginSerializer(user)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )
