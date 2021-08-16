from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, phone_number, password, **kwargs):
        if not phone_number:
            raise ValueError("Given phone number must be set")
        user = self.model(phone_number=phone_number, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone_number, password, **kwargs):
        kwargs.setdefault('is_staff', False)
        kwargs.setdefault('is_superuser', False)
        return self._create_user(phone_number, password, **kwargs)

    def create_superuser(self, phone_number, password, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_active', True)
        if kwargs.get('is_staff') is not True:
            return ValueError('Superuser must have status is_staff=True')
        if kwargs.get('is_superuser') is not True:
            return ValueError('Superuser must have status is_superuser=True')
        return self._create_user(phone_number, password, **kwargs)


class CustomUser(AbstractUser):
    phone_number = models.CharField('phone number', unique=True, max_length=20)
    password = models.CharField(max_length=100)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    objects = UserManager()
    username = models.CharField(max_length=255, blank=True)
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.phone_number
