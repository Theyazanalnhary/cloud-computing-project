from django.db import models

# Create your models here.
from django.db import models

class PoliceStructure(models.Model):
    department_id = models.AutoField(primary_key=True, verbose_name="رقم القسم")  # المفتاح الأساسي
    department_name = models.CharField(max_length=100, verbose_name="اسم قسم الشرطة")
    directorate_security = models.CharField(max_length=100, verbose_name="إدارة أمن المديرية")
    province_security = models.CharField(max_length=100, verbose_name="إدارة أمن المحافظة")

    def __str__(self):
        return f"قسم شرطة: {self.department_name}"

    class Meta:
        verbose_name = "قسم شرطة"
        verbose_name_plural = "الأقسام الشرطية"