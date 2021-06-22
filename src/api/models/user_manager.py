"""
user_manager.py
"""

from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy


class UserManager(BaseUserManager):
    """
    class UserManager(BaseUserManager)
    """

    def create_user(self, email, password, **extra_fields):
        """
        def create_user(self, email, password, **extra_fields)
        """

        if not email:
            raise ValueError(ugettext_lazy("Every user must have an email."))

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        def create_superuser(self, email, password, **extra_fields)
        """

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_superuser") is not True:
            raise ValueError(ugettext_lazy("Superusers must have is_superuser=True."))

        if extra_fields.get("is_staff") is not True:
            raise ValueError(ugettext_lazy("Superusers must have is_staff=True."))

        return self.create_user(email, password, **extra_fields)
