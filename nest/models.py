from django.db import models

from account.models import NestifyUser


class Nest(models.Model):
  user = models.OneToOneField(NestifyUser, on_delete=models.CASCADE)
  max_rooms = models.IntegerField(default=1)
  room_count = models.IntegerField(default=1)
  created_at = models.DateTimeField(auto_now_add=True)
  
  def __str__(self):
    return f"{self.user.name}'s Nest"
  
  def save(self, *args, **kwargs):
    if self.user.membership:
      self.max_rooms = self.user.membership.max_rooms
    super().save(*args, **kwargs)
  

class Room(models.Model):
  nest = models.ForeignKey(Nest, related_name="rooms", on_delete=models.CASCADE)
  name = models.CharField(max_length=100)
  created_at = models.DateTimeField(auto_now_add=True)
  
  def __str__(self):
    return f"Room {self.name} in {self.nest.user.name}'s Nest"