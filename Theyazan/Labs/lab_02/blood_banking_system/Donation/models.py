
from django.db import models
from datetime import timedelta

from Donors.models import Donor
from User.models import User
# جدول التبرعات
class Donation(models.Model):
    # خيارات الحالة الخاصة بالتبرع
    STATUS_CHOICES = [
        ('Tested', 'تم الفحص'),
        ('Unprocessed', 'غير معالج'),
        ('Stored', 'مخزن'),
        ('Expired', 'منتهي الصلاحية'),
    ]
    
    # تعريف الحقول
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE, related_name='donations')  # المتبرع الذي قام بالتبرع
    donation_date = models.DateField()  # تاريخ التبرع
    blood_type = models.CharField(max_length=3, choices=Donor.BLOOD_TYPES)  # فصيلة الدم المتبرع بها
    volume_in_ml = models.PositiveIntegerField()  # حجم التبرع بالملليتر
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)  # حالة التبرع
    processed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='processed_donations')  # الموظف الذي عالج التبرع

    # عند حفظ التبرع، إذا كانت حالته "مخزن"، يتم إضافة السجل إلى المخزون.
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # حفظ التبرع
        if self.status == 'Stored':  # إذا كانت حالة التبرع "مخزن"
            # إضافة سجل جديد في المخزون بناءً على التبرع
            Inventory.objects.create(
                blood_type=self.blood_type,  # فصيلة الدم
                quantity_in_ml=self.volume_in_ml,  # كمية الدم بالملليتر
                expiry_date=self.donation_date + timedelta(days=30),  # تاريخ انتهاء الصلاحية بعد 30 يوم
                status='Available',  # الحالة هي "متوفر"
                donation=self  # ربط المخزون بالتبرع
            )

    def __str__(self):
        return f"Donation by {self.donor.full_name} on {self.donation_date}"
