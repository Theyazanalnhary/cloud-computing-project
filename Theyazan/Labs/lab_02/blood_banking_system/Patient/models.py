from django.db import models
from Donors.models import Donor

# Create your models here.
# جدول المرضى
class Patient(models.Model):
    # خيارات الجنس وفصائل الدم التي تم تحديدها سابقًا
    GENDER_CHOICES = Donor.GENDER_CHOICES
    BLOOD_TYPES = Donor.BLOOD_TYPES
    
    # تعريف الحقول
    full_name = models.CharField(max_length=100)  # الاسم الكامل للمريض
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)  # الجنس (ذكر أو أنثى)
    date_of_birth = models.DateField()  # تاريخ الميلاد
    blood_type = models.CharField(max_length=3, choices=BLOOD_TYPES)  # فصيلة الدم
    contact_number = models.CharField(max_length=15, blank=True, null=True)  # رقم الاتصال (اختياري)
    address = models.TextField()  # العنوان
    medical_condition = models.TextField()  # الحالة الطبية للمريض
    created_at = models.DateTimeField(auto_now_add=True)  # تاريخ إنشاء سجل المريض

    def __str__(self):
        return self.full_name
