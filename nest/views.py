from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, NotFound, AuthenticationFailed
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
  CreateRoomSerializer,
  NestSerializer,
  CreateNestSerializer,
  RoomSerializer,
)
from .models import Nest, Room


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
  
  
class CreateListRoomView(APIView):
  def get(self, request, nest_id, *args, **kwargs):
    if not Nest.objects.filter(pk=nest_id).exists():
      raise NotFound(f"Nest with {nest_id} does not exist.")
    nest = Nest.objects.filter(pk=nest_id).first()
    if request.user.id != nest.user.id:
      raise AuthenticationFailed()
    rooms = Room.objects.filter(nest_id=nest_id).all()
    serializer = RoomSerializer(rooms, many=True)
    response = Response({"rooms": serializer.data}, status=HTTP_200_OK)
    return response
  
  def post(self, request, nest_id, *args, **kwargs):
    if not Nest.objects.filter(pk=nest_id).exists():
      raise NotFound(f"Nest with {nest_id} does not exist.")
    nest = Nest.objects.filter(pk=nest_id).first()
    if request.user.id != nest.user.id:
      raise AuthenticationFailed()
    if nest.max_rooms <= nest.room_count:
      raise AuthenticationFailed("The number of existed rooms already hits the maximum number of rooms")
    serializer = CreateRoomSerializer(data=request.data)
    
    if not serializer.is_valid():
      raise ValidationError(serializer.errors)
    
    if not Room.objects.filter(nest_id=nest_id).exists():
      serializer.validated_data['is_base'] = True
    else:
      serializer.validated_data['is_base'] = False
      
    
    room = serializer.create(serializer.validated_data)
    nest.room_count += 1
    nest.save()
    
    room_serializer = RoomSerializer(room)
    response = Response({'rooms': [room_serializer.data]}, status=HTTP_201_CREATED)
    return response


class DeleteRetrieveRoomView(APIView):
  def delete(self, request, nest_id, room_id, *args, **kwargs):
    if not Room.objects.filter(nest_id=nest_id, pk=room_id).exists():
      raise NotFound(f"Room with id {room_id} in Nest {nest_id} does not exist.")
    room = Room.objects.filter(pk=room_id).first()
    if request.user.id != room.nest.user.id:
      raise AuthenticationFailed(f"You do not have access to this room.")
    nest = room.nest
    room.delete()
    
    nest.room_count -= 1
    nest.save()
    response = Response({}, status=HTTP_204_NO_CONTENT)
    return response
    
  def get(self, request, nest_id, room_id, *args, **kwargs):
    if not Room.objects.filter(nest_id=nest_id, pk=room_id).exists():
      raise NotFound(f"Room with id {room_id} in Nest {nest_id} does not exist.")
    room = Room.objects.filter(pk=room_id).first()
    if request.user.id != room.nest.user.id:
      raise AuthenticationFailed(f"You do not have access to this room.")
    serializer = RoomSerializer(room)
    response = Response({'rooms': [serializer.data]}, status=HTTP_200_OK)
    return response
