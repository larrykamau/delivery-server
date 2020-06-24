from django.db import models
from django.db.models import Q, Value
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import datetime

class CustomUserManager(BaseUserManager):
    def create_user(
        self, email, password=None, is_staff=False, is_active=True, **extra_fields
    ):
        """Create a user instance with the given email and password."""
        email = CustomUserManager.normalize_email(email)
        # Google OAuth2 backend send unnecessary username field
        extra_fields.pop("username", None)

        user = self.model(
            email=email, is_active=is_active, is_staff=is_staff, **extra_fields
        )
        if password:
            user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        return self.create_user(
            email, password, is_staff=True, is_superuser=True, **extra_fields
        )

    def customers(self):
        return self.get_queryset().filter(
            Q(is_staff=False) | (Q(is_staff=True) & Q(orders__isnull=False))
        )

    def rider(self):
        return self.get_queryset().filter(
            Q(is_staff=False) | (Q(is_staff=True) & (Q(is_rider=False)) & Q(orders__isnull=False))
        )

    def staff(self):
        return self.get_queryset().filter(is_staff=True)
