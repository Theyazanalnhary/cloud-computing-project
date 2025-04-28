from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    is_police = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True) 