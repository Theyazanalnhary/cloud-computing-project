from django.db import models
from django.core.exceptions import ValidationError
from crimes.models import Crime
from investigations.models import Investigation  # استيراد نموذج إجراء التحري

class Prosecution(models.Model):
    prosecution_id = models.AutoField(primary_key=True, verbose_name="رقم الإجراء")
    crime = models.ForeignKey(Crime, on_delete=models.CASCADE, related_name="prosecutions", verbose_name="الجريمة")
    investigation = models.ForeignKey(
        Investigation,
        on_delete=models.CASCADE,
        related_name="prosecutions",
        verbose_name="إجراء التحري"
    )
    prosecutor_office = models.CharField(max_length=100, verbose_name="النيابة المختصة")
    case_number = models.CharField(max_length=50, verbose_name="رقم القضية")
    submission_date = models.DateField(verbose_name="تاريخ تقديم القضية للنيابة")
    prosecutor_decisions = models.TextField(verbose_name="قرارات النيابة")
    referral_to_court_date = models.DateField(blank=True, null=True, verbose_name="تاريخ الإحالة إلى المحكمة")
    court_procedures = models.TextField(blank=True, null=True, verbose_name="إجراءات المحكمة")
    verdict = models.TextField(blank=True, null=True, verbose_name="منطوق الحكم")
    sentence_execution = models.TextField(blank=True, null=True, verbose_name="تنفيذ العقوبة")

    def clean(self):
        # التحقق من أن الحقول crime و investigation موجودة
        if not hasattr(self, 'crime') or not hasattr(self, 'investigation'):
            raise ValidationError("يجب تحديد الجريمة وإجراء التحري.")

        # منع تكرار إجراء النيابة لنفس إجراء التحري
        query = Prosecution.objects.filter(crime=self.crime, investigation=self.investigation)
        if self.pk:  # إذا كان الكائن موجودًا بالفعل (أي أثناء التعديل)
            query = query.exclude(pk=self.pk)
        if query.exists():
            raise ValidationError("هذا إجراء التحري لديه بالفعل إجراء نيابة مسجل لهذه الجريمة!")

    def save(self, *args, **kwargs):
        self.full_clean()  # التحقق من صحة البيانات قبل الحفظ
        super().save(*args, **kwargs)

    def __str__(self):
        return f"إجراء نيابة رقم: {self.prosecution_id} - الجريمة: {self.crime.report_number} - التحري: {self.investigation.investigation_id}"

    class Meta:
        verbose_name = "إجراء نيابة"
        verbose_name_plural = "إجراءات النيابة"
        unique_together = ('crime', 'investigation')  # ضمان عدم التكرار