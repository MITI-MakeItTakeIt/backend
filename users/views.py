from rest_framework import status, views
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError

from utils.user_activate_token_generator import user_activation_token
from utils.custom_emails import UserActivationEmail
from utils.custom_responses import UserInfoCheckResponse

from .serializers import *

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
        email.send()
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
