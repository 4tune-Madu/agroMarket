
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True)

    is_buyer = models.BooleanField(default=True)
    is_seller = models.BooleanField(default=False)

    REQUIRED_FIELDS = ['email']
