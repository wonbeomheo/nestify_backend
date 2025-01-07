from django.db import models
from django.core.validators import MinValueValidator

from account.models import NestifyUser
from nest.models import Room


class Item(models.Model):
  name = models.CharField(max_length=100)
  description = models.TextField()
  price = models.DecimalField(max_digits=10, decimal_places=0)
  created_at = models.DateTimeField(auto_now_add=True)
  
  def __str__(self):
    return self.name
  

class Property(models.Model):
  class Meta:
    unique_together = ("name", "value")
    
  name = models.CharField(max_length=100, unique=True)
  value = models.ForeignKey('PropertyValue', on_delete=models.CASCADE, related_name="values")
  
  def __str__(self):
    return self.name
  
  
class PropertyValue(models.Model):
  value = models.CharField(max_length=100)
    
  def __str__(self):
    return f"{self.property.name}: {self.value}"
  

class PropertyAssignment(models.Model):
  item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="properties")
  property = models.ForeignKey(Property, on_delete=models.CASCADE)
  
  class Meta:
    unique_together = ("item", "property")
    
  def __str__(self):
    return f"{self.item.name} - {self.property.name}"


class ItemPurchased(models.Model):
  user = models.ForeignKey(NestifyUser, related_name='purchases', on_delete=models.CASCADE)
  item = models.ForeignKey(Item, on_delete=models.CASCADE)
  quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)], default=1)
  purchased_at = models.DateTimeField(auto_now_add=True)
  
  def __str__(self):
    return f"{self.user.name} purchased {self.item.name} at {self.purchased_at}"
  
  
class RoomItemPurchasedAssignment(models.Model):
  room = models.ForeignKey(Room, related_name='room_items', on_delete=models.CASCADE)
  item_purchased = models.ForeignKey(ItemPurchased, on_delete=models.CASCADE)
  position_x = models.FloatField(default=0)
  position_y = models.FloatField(default=0)
  position_z = models.FloatField(default=0)
  rotation_z = models.FloatField(default=0)
  created_at = models.DateTimeField(auto_now_add=True)
  
  def __str__(self):
    return f"Item {self.item_purchased.item.name} in {self.room.name}"
  

class Transaction(models.Model):
  TRANSACTION_TYPES = [
    ('puchase', 'Purchase'),
    ('reward', 'Reward'),
    ('refund', 'Refund'),
  ]
  
  user = models.ForeignKey(NestifyUser, related_name='transaction', on_delete=models.CASCADE)
  amount = models.DecimalField(max_digits=10, decimal_places=0)
  trans_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
  description = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)
  
  def __str__(self):
    return f"{self.user.name} {self.get_trans_type_display()} {self.amount} Nyms"
  