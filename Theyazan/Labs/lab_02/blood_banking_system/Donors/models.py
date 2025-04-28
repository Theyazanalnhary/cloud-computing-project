from django.db import models

# Create your models here.
# جدول المتبرعين
class Donor(models.Model):
    # خيارات الجنس
    GENDER_CHOICES = [
        ('Male', 'ذكر'),
        ('Female', 'أنثى'),
    ]
    
    # فصائل الدم المتاحة
    BLOOD_TYPES = [
        ('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-'),
    ]
    
    # تعريف الحقول
    full_name = models.CharField(max_length=100)  # الاسم الكامل للمتبرع
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)  # الجنس (ذكر أو أنثى)
    date_of_birth = models.DateField()  # تاريخ الميلاد
    blood_type = models.CharField(max_length=3, choices=BLOOD_TYPES)  # فصيلة الدم
    contact_number = models.CharField(max_length=15)  # رقم الاتصال
    email = models.EmailField(blank=True, null=True)  # البريد الإلكتروني (اختياري)
    address = models.TextField()  # العنوان
    last_donation_date = models.DateField(blank=True, null=True)  # تاريخ آخر تبرع (اختياري)
    created_at = models.DateTimeField(auto_now_add=True)  # تاريخ إنشاء سجل المتبرع (يتم تعبئته تلقائيًا)
    
    def __str__(self):
        return self.full_name