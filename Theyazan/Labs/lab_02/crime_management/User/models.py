from django.db import models
from django.contrib.auth.models import User

class PoliceOfficer(models.Model):
    ROLE_CHOICES = [
        ('مدير', 'مدير'),
        ('مدخل بيانات', 'مدخل بيانات'),
        ('معدل', 'معدل'),
        ('مسؤول تقارير', 'مسؤول تقارير'),
    ]

    officer_number = models.CharField(max_length=20, unique=True)
    full_name = models.CharField(max_length=100)
    rank = models.CharField(max_length=50)
    id_number = models.CharField(max_length=20, unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, related_name='created_officers', null=True, on_delete=models.SET_NULL)
    updated_by = models.ForeignKey(User, related_name='updated_officers', null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.full_name} - {self.role}"