from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import random

class NestifyUserManager(BaseUserManager):
  def get_random_username(self):
    number = random.randrange(1, 999)
    str_num = str(number).zfill(3)
    return f'user-{str_num}'
  
  def _create_user(self, email, password=None, **kwargs):
    kwargs.setdefault("username", self.get_random_username())
    
    if not email:
      raise ValueError("The given email must be set")
    
    email = self.normalize_email(email)
    
    user = NestifyUser(email=email, **kwargs)
    user.set_password(password)
    user.save()
    return user
  
  def create_user(self, email, password=None, **kwargs):
    kwargs.setdefault("is_staff", False)
    kwargs.setdefault("is_superuser", False)
    return self._create_user(email, password, **kwargs)
  
  def create_superuser(self, email, password=None, **kwargs):
    kwargs.setdefault("is_staff", True)
    kwargs.setdefault("is_superuser", True)
    
    if kwargs.get("is_staff") is not True:
      raise ValueError("Superuser must have is_staff=True")
    if kwargs.get("is_superuser") is not True:
      raise ValueError("Superuser must have is_superuser=True")
    return self._create_user(email, password, **kwargs)
    
class NestifyUser(AbstractBaseUser, PermissionsMixin):
  username = models.CharField(max_length=100, blank=False, null=False)
  name = models.CharField(max_length=255, blank=False, null=False)
  email = models.EmailField(null=False, blank=False, unique=True)
  balance = models.DecimalField(max_digits=10, decimal_places=0, default=0)
  membership = models.ForeignKey('Membership', on_delete=models.SET_NULL, null=True, blank=True)
  is_staff = models.BooleanField(default=False)
  is_superuser = models.BooleanField(default=False)
  
  USERNAME_FIELD = 'email'
  
  objects = NestifyUserManager()


class Membership(models.Model):
  """
    Nestify Membership
    
    - Nestian
    - Free
  """
  MEMBERSHIP_TYPES = [
    ('free', 'Free'),
    ('nestian', 'Nestian'),
  ]
  
  name = models.CharField(max_length=10, choices=MEMBERSHIP_TYPES, default='free')
  max_rooms = models.IntegerField(default=1)
  description = models.TextField()
  
  def __str__(self):
    return self.name
  
  