from rest_framework.serializers import ModelSerializer
from .models import Item, Property, PropertyAssignment, PropertyValue


class PropertySerializer(ModelSerializer):
  class Meta:
    model = Property
    fields = '__all__'
    

class PropertyValueSerializer(ModelSerializer):
  property = PropertySerializer(many=False)
  
  class Meta:
    model = PropertyValue
    fields = '__all__'


class PropertyAssignmentSerializer(ModelSerializer):
  class Meta:
    model = PropertyAssignment
    fields = ('id', 'property', 'value', 'item')
    read_only_fields = ('id', 'item')

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
  properties = PropertyAssignmentSerializer(many=True)
  
  class Meta:
    model = Item
    fields = ('properties',)
  
  def update(self, instance, validated_data):
    requested_properties = validated_data.pop('properties', [])
    existing_assignments = instance.properties.all()
    # key: property, value: value
    requested_properties_map = {
      prop['property']: prop['value'] for prop in requested_properties
    }
    
    print(requested_properties)
    for assignment in existing_assignments:
      if assignment.property.id not in requested_properties_map or assignment.property_value.id != requested_properties_map[assignment.property.id]:
        assignment.delete()
      
    
    for property, value in requested_properties_map.items():
      print(property)
      if not existing_assignments.filter(property=property, value=value).exists():
        PropertyAssignment.objects.create(
          item=instance,
          property=property,
          value=value
        )
    
    instance.save()
    return instance