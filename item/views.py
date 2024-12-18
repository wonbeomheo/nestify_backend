from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.status import (
  HTTP_200_OK,
  HTTP_201_CREATED,
  HTTP_204_NO_CONTENT,
)

from .serializers import CreateItemSerializer, ItemPropertySerializer, ItemPropertyValueSerializer, ItemSerializer, UpdateItemSerializer
from .models import Item, ItemProperty, ItemPropertyValue


class CreateListItem(APIView):
  def get(self, request, *args, **kwargs):
    items = Item.objects.prefetch_related('properties').all()
    serializer = ItemSerializer(items, many=True)
    response = Response({'items': serializer.data}, status=HTTP_200_OK)
    return response
  
  def post(self, request, *args, **kwargs):
    serializer = CreateItemSerializer(data=request.data)
    if not serializer.is_valid():
      raise ValidationError(serializer.errors)
    item = serializer.create(serializer.validated_data)
    serialized_item = ItemSerializer(item)
    response = Response({'items': serialized_item.data}, status=HTTP_201_CREATED)
    return response
  

class DeleteRetrieveItem(APIView):
  def get(self, request, id, *args, **kwargs):
    if not Item.objects.filter(pk=id).exists():
      raise ValidationError(f"No item with id {id} found.")
    item = Item.objects.filter(pk=id).first()
    serializer = ItemSerializer(item)
    response = Response({'items': [serializer.data]}, status=HTTP_200_OK)
    return response
  
  def delete(self, request, id, *args, **kwargs):
    if not Item.objects.filter(pk=id).exists():
      raise ValidationError(f"No item with id {id} found.")
    item = Item.objects.filter(pk=id).first()
    item.delete()
    response = Response({}, status=HTTP_204_NO_CONTENT)
    return response
  
  def put(self, request, id, *args, **kwargs):
    if not Item.objects.filter(pk=id).exists():
      raise ValidationError(f"No item with id {id} found.")
    serializer = UpdateItemSerializer(data=request.data)
    if not serializer.is_valid():
      raise ValidationError(serializer.errors)
    item = Item.objects.filter(pk=id).first()
    updated_item = serializer.update(item, serializer.validated_data)
    serialized_updated_item = ItemSerializer(updated_item)
    return Response({"items": [serialized_updated_item.data]}, status=HTTP_200_OK)
  
  
class CreateListPropertyValue(APIView):
  def get(self, request, *args, **kwargs):
    property_value_list = ItemPropertyValue.objects.all()
    # property_value_list = ItemProperty.objects.prefetch_related('values').all()
    # serializer = ItemPropertySerializer(property_value_list, many=True)
    serializer = ItemPropertyValueSerializer(property_value_list, many=True)
    response = Response({"properties": serializer.data}, status=HTTP_200_OK)
    return response
  
  