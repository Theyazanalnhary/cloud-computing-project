from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('admin', 'مدير النظام'),
        ('police', 'ضابط شرطة'),
        ('investigator', 'محقق'),
    )
    
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    phone_number = models.CharField(max_length=20, blank=True)
    department = models.CharField(max_length=100, blank=True)
    badge_number = models.CharField(max_length=50, blank=True)
    
    def __str__(self):
        return f"{self.get_full_name()} - {self.get_user_type_display()}" 