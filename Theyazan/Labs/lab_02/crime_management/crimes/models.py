from django.db import models

class Crime(models.Model):
    report_number = models.CharField(max_length=50, unique=True, verbose_name="رقم البلاغ")  # المفتاح الأساسي
    description = models.TextField(verbose_name="وصف البلاغ")
    report_date = models.DateField(verbose_name="تاريخ البلاغ")
    reporter_name = models.CharField(max_length=100, verbose_name="اسم المبلغ")
    reporter_phone = models.CharField(max_length=20, verbose_name="رقم هاتف المبلغ")
    crime_date = models.DateField(verbose_name="تاريخ وقوع الجريمة")
    crime_time = models.TimeField(verbose_name="ساعة الوقوع")
    crime_type = models.CharField(max_length=100, verbose_name="نوع الجريمة")
    location = models.CharField(max_length=200, verbose_name="مكان الجريمة")
    tool_used = models.CharField(max_length=100, blank=True, null=True, verbose_name="أداة الجريمة")
    method = models.TextField(verbose_name="أسلوب التنفيذ")
    motives = models.TextField(blank=True, null=True, verbose_name="دوافع الجريمة")
    causes = models.TextField(blank=True, null=True, verbose_name="أسباب الجريمة")
    summary = models.TextField(verbose_name="ملخص الجريمة")
    confiscated_items = models.TextField(blank=True, null=True, verbose_name="مضبوطات")
    recovered_items = models.TextField(blank=True, null=True, verbose_name="مستردات")

    def __str__(self):
        return f"بلاغ رقم: {self.report_number}"

    class Meta:
        verbose_name = "جريمة"
        verbose_name_plural = "الجرائم"