from django.db import models



# نموذج التقرير (Report)
class Report(models.Model):
    # معرف التقرير
    report_id = models.AutoField(primary_key=True)  # مفتاح أساسي يتم توليده تلقائيًا
    title = models.CharField(max_length=100)  # عنوان التقرير
    created_by = models.IntegerField()  # معرف الموظف الذي أنشأ التقرير
    created_date = models.DateTimeField()  # تاريخ إنشاء التقرير
    content = models.TextField()  # محتوى التقرير

    # تمثيل النصي للتقرير
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Report"  # الاسم المفرد للكيان
        verbose_name_plural = "Reports"  # الاسم الجمعي للكيان
