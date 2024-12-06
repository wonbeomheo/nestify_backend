from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError, NotFound, APIException
from rest_framework.permissions import IsAuthenticated
from django.core import serializers as django_serializers
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope


from .models import NestifyUser
from .serializers import (
  UserSerializer,
  UserCreateSerializer,
  UserUpdateSerializer,
)
from rest_framework.response import Response
from rest_framework.status import (
  HTTP_200_OK,
  HTTP_201_CREATED,
  HTTP_204_NO_CONTENT,
  HTTP_400_BAD_REQUEST,
  HTTP_401_UNAUTHORIZED,
  HTTP_403_FORBIDDEN,
  HTTP_404_NOT_FOUND,
  HTTP_500_INTERNAL_SERVER_ERROR,
)


class UserListRegisterView(APIView):
  permission_classes = [IsAuthenticated, TokenHasReadWriteScope]
  
  def post(self, request):
    serializer = UserCreateSerializer(data=request.data)
    if not serializer.is_valid():
      raise ValidationError(serializer.errors)
    try:
      user = serializer.create(serializer.validated_data)
      serialized_data = UserSerializer(user).data
    except Exception as e:
      NestifyUser.objects.filter(pk=user.id).delete()
      raise APIException(e)
    return Response({"users": serialized_data}, status=HTTP_201_CREATED)
  
  def get(self, request):
    queryset = NestifyUser.objects.all()
    serializer = UserSerializer(queryset, many=True)
    users = serializer.data
    
    return Response({"users": users}, status=HTTP_200_OK)
  

class UserDetailDeleteView(APIView):
  permission_classes = [IsAuthenticated, TokenHasReadWriteScope]
  def get(self, request, id):
    if not NestifyUser.objects.filter(pk=id).exists():
      raise NotFound(f'There is no user with id {id}')
    user = NestifyUser.objects.filter(pk=id).first()
    try:
      response = Response({"users": [UserSerializer(user).data]}, status=HTTP_200_OK)
    except Exception as e:
      raise APIException(e)
    return response
  
  def delete(self, request, id):
    if not NestifyUser.objects.filter(pk=id).exists():
      raise NotFound(f'There is no user with id {id}')
    NestifyUser.objects.filter(pk=id).delete()
    response = Response({}, status=HTTP_204_NO_CONTENT)
    return response
  
  def put(self,request, id):
    if not NestifyUser.objects.filter(pk=id).exists():
      raise NotFound(f'There is no user with id {id}')
    serializer = UserUpdateSerializer(data=request.data)
    if not serializer.is_valid():
      raise ValidationError(serializer.errors)
    
    user = NestifyUser.objects.filter(pk=id).first()
    user = serializer.update(user, validated_data=serializer.validated_data)
    serialized_data = UserSerializer(user).data
    response = Response({"users": [serialized_data]}, status=HTTP_200_OK)
    return response
