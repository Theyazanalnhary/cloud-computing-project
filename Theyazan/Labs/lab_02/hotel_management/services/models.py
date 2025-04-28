from django.db import models

# Create your models here.
# نموذج الخدمة (Service)
class Service(models.Model):
    # معرف الخدمة
    service_id = models.AutoField(primary_key=True)  # مفتاح أساسي يتم توليده تلقائيًا
    service_name = models.CharField(max_length=100)  # اسم الخدمة
    price = models.DecimalField(max_digits=10, decimal_places=2)  # السعر
    description = models.TextField()  # وصف الخدمة

    # تمثيل النصي للخدمة
    def __str__(self):
        return self.service_name

    class Meta:
        verbose_name = "Service"  # الاسم المفرد للكيان
        verbose_name_plural = "Services"  # الاسم الجمعي للكيان

