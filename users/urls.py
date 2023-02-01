from django.urls import path

from .views import *

urlpatterns = [
    path('', UserListView.as_view()),
    path('activate/<str:uidb64>/<str:token>/', UserActivateView.as_view()),
    path('user-info-check/', UserInfoCheckView.as_view(), name="user-info-check"),
]