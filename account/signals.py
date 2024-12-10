from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import NestifyUser
from nest.models import Nest, Room

@receiver(post_save, sender=NestifyUser)
def update_nest_max_rooms(sender, instance, **kwargs):
  """
    When a membership is modified for a user, update Nest's max_rooms
  """
  if instance.membership:
    try:
      nest = instance.nest
      rooms = Room.objects.filter(nest=nest).all()
      if instance.membership.id == 1:
        for room in rooms:
          if not room.is_base:
            room.is_activated = False
          else:
            room.is_activated = True
          room.save()
      else:
        for room in rooms:
          room.is_activated = True
          room.save()
      nest.max_rooms = instance.membership.max_rooms
      nest.save()
    except Nest.DoesNotExist:
      pass