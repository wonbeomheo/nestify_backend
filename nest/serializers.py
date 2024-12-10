from rest_framework.serializers import ModelSerializer
from .models import Nest, Room

class CreateNestSerializer(ModelSerializer):
  class Meta:
    model = Nest
    fields = ['user']


class NestSerializer(ModelSerializer):
  class Meta:
    model = Nest
    fields = '__all__'
    

class RoomSerializer(ModelSerializer):
  class Meta:
    model = Room
    fields = '__all__'
    

class CreateRoomSerializer(ModelSerializer):
  class Meta:
    model = Room
    fields = ['nest', 'name']
    