# staff/models.py
from django.contrib.auth.models import User
from django.db import models

class Staff(models.Model):
    ROLE_CHOICES = [
        ('lab_technician', 'Lab Technician'),
        ('nurse', 'Nurse'),
        ('doctor', 'Doctor'),
        ('manager', 'Manager')  # إضافة دور المدير
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone_number = models.CharField(max_length=20)
    password = models.CharField(max_length=20, null=True, blank=True)  # يعتبر هذا غير آمن
    date_of_joining = models.DateField()
    is_supervisor = models.BooleanField(default=False)  # حقل للتحقق مما إذا كان المستخدم هو المشرف الوحيد
    is_first_user = models.BooleanField(default=False)  # حقل لتحديد ما إذا كان المستخدم هو الأول

    def __str__(self):
        return self.user.username
        return self.name
