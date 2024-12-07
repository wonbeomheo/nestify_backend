from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.status import (
  HTTP_200_OK,
  HTTP_201_CREATED,
  HTTP_204_NO_CONTENT,
  HTTP_400_BAD_REQUEST,
  HTTP_401_UNAUTHORIZED,
  HTTP_404_NOT_FOUND,
  HTTP_500_INTERNAL_SERVER_ERROR
)
from .serializers import (
  NestSerializer,
  CreateNestSerializer,
)
from .models import Nest


class CreateNestView(APIView):
  def post(self, request, *args, **kwargs):
    serializer = CreateNestSerializer(data=request.data)
    if not serializer.is_valid():
      raise ValidationError(serializer.errors)
    nest = Nest.objects.create(**serializer.validated_data)
    response = Response({"nests": [NestSerializer(nest).data]}, status=HTTP_201_CREATED)
    return response
  
  def get(self, request, *args, **kwargs):
    nests = Nest.objects.all()
    serializer = NestSerializer(nests, many=True)
    response = Response({"nests": serializer.data}, status=HTTP_200_OK)
    return response


class RetrieveDeleteNestView(APIView):
  def get(self, request, id, *args, **kwargs):
    if not Nest.objects.filter(pk=id).exists():
      raise NotFound(f"Nest with id {id} does not exist.")
    nest = Nest.objects.filter(pk=id).first()
    serializer = NestSerializer(nest)
    response = Response({"nests": [serializer.data]}, status=HTTP_200_OK)
    return response
  
  def delete(self, request, id, *args, **kwargs):
    if not Nest.objects.filter(pk=id).exists():
      raise NotFound(f"Nest with id {id} does not exist.")
    Nest.objects.filter(pk=id).first().delete()
    response = Response({}, status=HTTP_204_NO_CONTENT)
    return response