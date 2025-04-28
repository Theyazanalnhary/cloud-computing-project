# استيراد المكتبات اللازمة من Django
from django.db import models  # استيراد مكتبة النماذج في Django
from django.utils import timezone  # استيراد timezone لإعداد التواريخ والأوقات الافتراضية

# نموذج العميل (Customer)
class Customer(models.Model):
    # معرف العميل
    customer_id = models.AutoField(primary_key=True)  # مفتاح أساسي يتم توليده تلقائيًا
    first_name = models.CharField(max_length=50)  # اسم العميل الأول
    last_name = models.CharField(max_length=50)  # اسم العميل الأخير
    email = models.EmailField(unique=True)  # البريد الإلكتروني للعميل مع التأكد من التفرد
    phone_number = models.CharField(max_length=15)  # رقم الهاتف
    address = models.TextField()  # عنوان العميل
    date_of_birth = models.DateField()  # تاريخ الميلاد
    registration_date = models.DateTimeField(default=timezone.now)  # تاريخ التسجيل (افتراضيًا الوقت الحالي)

    # تمثيل النصي للعميل
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Customer"  # الاسم المفرد للكيان
        verbose_name_plural = "Customers"  # الاسم الجمعي للكيان


