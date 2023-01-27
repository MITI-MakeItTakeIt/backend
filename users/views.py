from rest_framework import status, views
from rest_framework.response import Response
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str

from utils.user_activate_token_generator import user_activation_token
from utils.custom_emails import UserActivationEmail

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
        