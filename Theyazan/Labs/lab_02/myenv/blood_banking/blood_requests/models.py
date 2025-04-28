from django.db import models
from inventory.models import InventoryItem

class BloodRequest(models.Model):
    BLOOD_TYPE_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]

    # معلومات مقدم الطلب
    name = models.CharField(max_length=100, verbose_name="الاسم", default="unludd")
    email = models.EmailField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, verbose_name="رقم الهاتف", default="091133333")

    # معلومات الطلب
    blood_type = models.CharField(max_length=3, choices=BLOOD_TYPE_CHOICES, verbose_name="فصيلة الدم", default="A+")
    quantity = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="الكمية المطلوبة", default="00")
    request_date = models.DateField(auto_now_add=True, verbose_name="تاريخ الطلب")

    # حالة الطلب: مقبول أو مرفوض بناءً على المخزون
    STATUS_CHOICES = [
        ('pending', 'معلق'),
        ('approved', 'موافق عليه'),
        ('rejected', 'مرفوض'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending', verbose_name="حالة الطلب")

    def check_stock(self):
        """التحقق من المخزون للتأكد من وجود الكمية المطلوبة"""
        stock = InventoryItem.objects.filter(blood_type=self.blood_type).first()
        if stock and stock.quantity >= float(self.quantity):
            return True
        return False

    def save(self, *args, **kwargs):
        """التحقق من المخزون قبل حفظ الطلب"""
        if not self.pk:  # فقط عند إنشاء طلب جديد
            if not self.check_stock():
                raise ValueError("الكمية المطلوبة غير متوفرة في المخزون.")
        super().save(*args, **kwargs)

    def accept_request(self):
        """قبول الطلب إذا كان المخزون كافياً"""
        if self.check_stock():
            # تحديث حالة الطلب إلى "موافق عليه"
            self.status = 'approved'
            # تقليل الكمية في المخزون
            stock = InventoryItem.objects.get(blood_type=self.blood_type)
            stock.quantity -= float(self.quantity)
            stock.save()
            self.save()
            return True
        else:
            # إذا لم يكن المخزون كافياً
            self.status = 'rejected'
            self.save()
            return False

    def __str__(self):
        return f'طلب من {self.name} لفصيلة {self.blood_type} ({self.status})'