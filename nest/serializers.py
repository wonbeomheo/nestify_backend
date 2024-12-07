from rest_framework.serializers import ModelSerializer
from .models import Nest

class CreateNestSerializer(ModelSerializer):
  class Meta:
    model = Nest
    fields = ['user']


class NestSerializer(ModelSerializer):
  class Meta:
    model = Nest
    fields = '__all__'