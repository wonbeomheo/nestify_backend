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
  

class ItemProperty(models.Model):
  name = models.CharField(max_length=100, unique=True)
  
  def __str__(self):
    return self.name
  
  
class ItemPropertyValue(models.Model):
  property = models.ForeignKey(ItemProperty, on_delete=models.CASCADE, related_name="values")
  value = models.CharField(max_length=100)
  
  class Meta:
    unique_together = ("property", "value")
    
  def __str__(self):
    return f"{self.property.name}: {self.value}"
  

class ItemPropertyAssignment(models.Model):
  item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="properties")
  property = models.ForeignKey(ItemProperty, on_delete=models.CASCADE)
  value = models.ForeignKey(ItemPropertyValue, on_delete=models.CASCADE)
  
  class Meta:
    unique_together = ("item", "property")
    
  def __str__(self):
    return f"{self.item.name} - {self.property.name}: {self.value.value}"


class ItemPurchase(models.Model):
  user = models.ForeignKey(NestifyUser, related_name='purchases', on_delete=models.CASCADE)
  item = models.ForeignKey(Item, on_delete=models.CASCADE)
  quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)], default=1)
  purchased_at = models.DateTimeField(auto_now_add=True)
  
  def __str__(self):
    return f"{self.user.name} purchased {self.item.name} at {self.purchased_at}"
  
  
class RoomItem(models.Model):
  room = models.ForeignKey(Room, related_name='room_items', on_delete=models.CASCADE)
  item_purchase = models.ForeignKey(ItemPurchase, on_delete=models.CASCADE)
  position_x = models.FloatField(default=0)
  position_y = models.FloatField(default=0)
  position_z = models.FloatField(default=0)
  rotation_z = models.FloatField(default=0)
  created_at = models.DateTimeField(auto_now_add=True)
  
  def __str__(self):
    return f"Item {self.item_purchase.item.name} in {self.room.name}"
  

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
  