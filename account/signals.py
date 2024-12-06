from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import NestifyUser
from nest.models import Nest

@receiver(post_save, sender=NestifyUser)
def update_nest_max_rooms(sender, instance, **kwargs):
  """
    When a membership is modified for a user, update Nest's max_rooms
  """
  if instance.membership:
    try:
      nest = instance.nest
      nest.max_rooms = instance.membership.max_rooms
      nest.save()
    except Nest.DoesNotExist:
      pass