from django.db import models
from Donors.models import Donor
from Donation.models import Donation
# Create your models here.
# جدول المخزون
class Inventory(models.Model):
    # فصائل الدم المتاحة
    BLOOD_TYPES = Donor.BLOOD_TYPES
    # خيارات الحالة الخاصة بالمخزون
    STATUS_CHOICES = [
        ('Available', 'متوفر'),
        ('Reserved', 'محجوز'),
        ('Expired', 'منتهي الصلاحية'),
    ]
    
    # تعريف الحقول
    blood_type = models.CharField(max_length=3, choices=BLOOD_TYPES)  # فصيلة الدم المخزنة
    quantity_in_ml = models.PositiveIntegerField()  # كمية الدم المتاحة بالملليتر
    expiry_date = models.DateField()  # تاريخ انتهاء صلاحية الدم
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)  # حالة المخزون
    donation = models.ForeignKey(Donation, on_delete=models.CASCADE, related_name='inventory')  # ربط المخزون بالتبرع

    # دالة لفحص إذا كانت الكمية المتاحة في المخزون كافية لتلبية الطلب
    def check_availability(self, quantity):
        return self.quantity_in_ml >= quantity

    def __str__(self):
        return f"Inventory for {self.blood_type} ({self.quantity_in_ml} ml)"
