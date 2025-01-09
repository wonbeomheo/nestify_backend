from collections import defaultdict
from rest_framework.serializers import ModelSerializer, StringRelatedField, SerializerMethodField, ValidationError, CharField, IntegerField
from .models import Item, Property, PropertyAssignment, PropertyValue

    

class PropertyValueSerializer(ModelSerializer):
  class Meta:
    model = PropertyValue
    fields = '__all__'

class PropertySerializer(ModelSerializer):
  values = PropertyValueSerializer(many=True)
  
  class Meta:
    model = Property
    fields = '__all__'

class PropertyAssignmentSerializer(ModelSerializer):
  property_id = SerializerMethodField()
  value = StringRelatedField()
  
  class Meta:
    model = PropertyAssignment
    fields = ('id', 'property_id', 'value')
    read_only_fields = ('id', 'item',)
    
  def get_property_id(self, obj):
    return obj.value.property.id

  def validate_property_id(self, data):
    print(data)
    return data
    

class UpdatePropertyAssignmentSerializer(ModelSerializer):
  property_id = IntegerField()
  value = CharField(max_length=10)
  
  class Meta:
    model = PropertyAssignment
    fields = ('id', 'property_id', 'value')
    
  
  def validate_property_id(self, data):
    if not data:
      raise ValidationError("property_id cannot be empty.")
    if not Property.objects.filter(pk=data).exists():
      raise ValidationError(f"Property with id #{data} does not exists.")
    return data
  
  def validate(self, attrs):
    try:
      property_id = attrs['property_id']
      value = attrs['value']
    except KeyError:
      raise ValidationError("Required fields are missing. Required fields are: 'property_id' and 'value'.")
    
    if not PropertyValue.objects.filter(value=value, property=property_id).exists():
      raise ValidationError({"property_value_errors": "Please check the value is assigned to the property."})
    return attrs
  
class ItemSerializer(ModelSerializer):
  properties = PropertyAssignmentSerializer(many=True)
  
  class Meta:
    model = Item
    fields = '__all__'


class CreateItemSerializer(ModelSerializer):
  
  class Meta:
    model = Item
    fields = '__all__'
  
  def create(self, validated_data):
    item = Item.objects.create(**validated_data)
    return item
    
class UpdateItemSerializer(ModelSerializer):
  properties = UpdatePropertyAssignmentSerializer(many=True)
  
  class Meta:
    model = Item
    fields = ('properties',)
    
  def update(self, instance, validated_data):
    requested_properties = validated_data.pop('properties', [])
    existing_assignments = instance.properties.all()
    
    requested_hash = {}
    for requested_property in requested_properties:
      if requested_property['property_id'] not in requested_hash:
        requested_hash[requested_property['property_id']] = {requested_property['value']}
      requested_hash[requested_property['property_id']].add(requested_property['value'])
    
    for assignment in existing_assignments:
      if assignment.value.property.id in requested_hash and \
        assignment.value.value not in requested_hash[assignment.value.property.id]:
          assignment.delete()
    
    for property, values in requested_hash.items():
      for value in values:
        if PropertyValue.objects.prefetch_related('property').filter(value=value, property_id=property).exists():
          value_instance = PropertyValue.objects.prefetch_related('property').filter(value=value, property_id=property).first()
          if not PropertyAssignment.objects.filter(item=instance, value=value_instance).exists():
            PropertyAssignment.objects.create(
              item=instance,
              value=value_instance,
            )
    
    instance.save()
    return instance