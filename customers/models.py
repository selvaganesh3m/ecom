import binascii
import os

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.conf import settings


# 2 Models
# User, UserAddress
# from customers.utils import generate_jti


# def generate_jti():
#     return binascii.hexlify(os.urandom(32)).decode()
from customers.utils import generate_jti


class CustomUserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Email is must.")
        # endif
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("SuperUser Staff status must be True.")
        # endif
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Super user should be is_superuser=True.")
        # endif
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    jti = models.CharField(max_length=64, editable=False, default=generate_jti())

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class UserAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=10, unique=True)
    address_line1 = models.CharField(max_length=150)
    address_line2 = models.CharField(max_length=150)
    area = models.CharField(max_length=150)
    city = models.CharField(max_length=150)
    state = models.CharField(max_length=150)
    country = models.CharField(max_length=150)
    pincode = models.CharField(max_length=6)

    class Meta:
        verbose_name_plural = 'User Addresses'

    def __str__(self):
        return self.first_name + self.last_name
