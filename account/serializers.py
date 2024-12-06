from rest_framework.serializers import HyperlinkedModelSerializer, ModelSerializer, CharField, ValidationError
from rest_framework.mixins import ListModelMixin

from .models import NestifyUser

class UserSerializer(ModelSerializer, ListModelMixin):
  class Meta:
    model = NestifyUser()
    fields = ['id', 'name', 'email', 'last_login', 'is_staff', 'is_superuser']
    
class UserCreateSerializer(ModelSerializer):
  password2 = CharField(
    write_only=True,
    style={
      'input_type': 'password',
    }
  )
  
  class Meta:
    model = NestifyUser
    fields = '__all__'
    extra_kwargs = {'password': {'write_only': True}}
  
  def validate(self, data):
    password = data.get('password')
    password2 = data.get('password2')
    if password != password2:
      raise ValidationError({
        'password': ['Passwords do not match.'],
        'password2': ['Passwords do not match.']
      }, code='mismatch')
    del data['password2']
    return data
  
  def create(self, validated_data):
    user = NestifyUser.objects.create_user(
      **validated_data
    )
    return user
  
class UserUpdateSerializer(HyperlinkedModelSerializer):
  class Meta:
    model = NestifyUser
    fields = ['is_staff']
    