"""
user.py
"""

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy
from api.models.user_manager import UserManager


class User(AbstractUser):
    """
    class User(AbstractUser)
    """

    username = None
    first_name = None
    last_name = None

    email = models.EmailField(ugettext_lazy("Email address"), unique=True,
                              error_messages={"unique": "An account with that email address already exists."})

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()
