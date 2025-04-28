from django.db import models

# جدول المستخدمين
class User(models.Model):
    # خيارات الأدوار للمستخدمين: مسؤول، مشرف، موظف
    ROLE_CHOICES = [
        ('Admin', 'مسؤول'),
        ('Supervisor', 'مشرف'),
        ('Staff', 'موظف'),
    ]
    
    # تعريف الحقول
    username = models.CharField(max_length=50, unique=True)  # اسم المستخدم (يجب أن يكون فريد)
    password = models.CharField(max_length=255)  # كلمة المرور
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)  # دور المستخدم (مسؤول، مشرف، موظف)
    full_name = models.CharField(max_length=100)  # الاسم الكامل
    email = models.EmailField(unique=True)  # البريد الإلكتروني (يجب أن يكون فريد)
    phone_number = models.CharField(max_length=15, blank=True, null=True)  # رقم الهاتف (اختياري)
    created_at = models.DateTimeField(auto_now_add=True)  # تاريخ إنشاء الحساب (يتم تعبئته تلقائيًا)
    
    def __str__(self):
        return self.username

