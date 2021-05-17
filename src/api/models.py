from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy

FEATURE_TYPES = (
    ("park","park"),
    ("pond", "pond"),
    ("citysquares", "squares"),
    ("forest", "forest"),
    ("urbanforest", "urbanf"),
    ("nationalpark", "nationalp"),
)

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


class Tile(models.Model):
    tid = models.AutoField(primary_key=True)
    x_coordinate = models.DecimalField(max_digits=9, decimal_places=6)
    y_coordinate = models.DecimalField(max_digits=9, decimal_places=6)
    #year = models.IntegerField()

class Classification(models.Model):
    tile = models.ForeignKey(Tile, db_column="tid", on_delete=models.CASCADE)
    label = models.CharField(max_length=30)
    #type = models.CharField(choices=FEATURE_TYPES, default=None, max_length=30)
    year = models.IntegerField()



