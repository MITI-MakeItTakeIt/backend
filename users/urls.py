from django.urls import path

from .views import *

urlpatterns = [
    path('', UserListView.as_view()),
    path('activate/<str:uidb64>/<str:token>/', UserActivateView.as_view()),
]