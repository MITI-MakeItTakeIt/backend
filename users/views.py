from rest_framework import status, views
from rest_framework.response import Response

from .serializers import *


# Create your views here.

class UserListView(views.APIView):
    
    def post(self, request):
        serializer = UserBaseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)