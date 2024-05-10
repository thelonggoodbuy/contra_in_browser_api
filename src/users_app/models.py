from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.mail import send_mail

from .managers import CustomUserManager

# from ads.models import Ads, Accomodation



class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=200, unique=True)
    email = models.EmailField(unique=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    total_score = models.BigIntegerField(default=0)


    objects = CustomUserManager()
    USERNAME_FIELD = "username"