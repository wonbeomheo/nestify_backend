from django.urls import path
from .views import (
  UserListRegisterView,
  UserDetailDeleteView,
)

urlpatterns = [
    path('', UserListRegisterView.as_view(), name='users'),
    path('<int:id>', UserDetailDeleteView.as_view(), name='user')
]
