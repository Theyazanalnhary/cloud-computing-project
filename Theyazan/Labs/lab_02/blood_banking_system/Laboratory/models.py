from django.db import models

# Create your models here.
# جدول المختبرات
class Laboratory(models.Model):
    # تعريف الحقول
    name = models.CharField(max_length=100)  # اسم المختبر
    location = models.TextField()  # موقع المختبر
    contact_number = models.CharField(max_length=15)  # رقم الاتصال
    created_at = models.DateTimeField(auto_now_add=True)  # تاريخ إنشاء سجل المختبر
    
    def __str__(self):
        return self.name