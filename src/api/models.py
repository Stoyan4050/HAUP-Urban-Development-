from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy

class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(ugettext_lazy("Every user must have an email."))
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(ugettext_lazy("Superusers must have is_superuser=True."))
        
        if extra_fields.get("is_staff") is not True:
            raise ValueError(ugettext_lazy("Superusers must have is_staff=True."))
        
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    username = None
    first_name = None
    last_name = None
    
    email = models.EmailField(ugettext_lazy("Email address"), unique=True, error_messages={"unique": "An account with that email address already exists."})
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

# Create your models here.


class TileManager(models.Manager):
    def create_tile(self, url, label, year):
        if not url:
            raise ValueError(ugettext_lazy("You can't save tile without URL"))

        tile = self.create(url=url, label=label, year=year)
        return tile


class Tile(models.Model):
    url = models.CharField(max_length=200)
    label = models.CharField(max_length=50)
    year = models.IntegerField()
    REQUIRED_FIELDS = [url, label]
    objects = TileManager()

