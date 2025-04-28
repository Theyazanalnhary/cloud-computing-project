from django.db import models
from crimes.models import Crime
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator

class Victim(models.Model):
    """
    نموذج يمثل المجني عليه في النظام
    """
    GENDER_CHOICES = [('ذكر', 'ذكر'), ('أنثى', 'أنثى')]
    MARITAL_STATUS = [('أعزب', 'أعزب'), ('متزوج', 'متزوج')]
    
    victim_id = models.AutoField(primary_key=True, verbose_name="رقم المجني عليه")
    
    # تغيير العلاقة إلى ManyToMany بدلاً من ForeignKey
    crimes = models.ManyToManyField(
        Crime, 
        related_name="victims",
        verbose_name="الجرائم المرتبطة"
    )
    
    full_name = models.CharField(max_length=100, verbose_name="الاسم الثلاثي")
    nickname = models.CharField(max_length=50, blank=True, null=True, verbose_name="اللقب")
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, verbose_name="الجنس")
    nationality = models.CharField(max_length=50, verbose_name="الجنسية")
    country = models.CharField(max_length=50, verbose_name="البلد")
    age = models.PositiveIntegerField(
        verbose_name="العمر",
        validators=[
            MinValueValidator(1),
            MaxValueValidator(120)
        ]
    )
    residence = models.CharField(max_length=200, verbose_name="محل الإقامة")
    phone = models.CharField(
        max_length=20, 
        verbose_name="رقم الهاتف",
        validators=[
            RegexValidator(
                regex='^7\d{8}$',
                message='يجب أن يبدأ رقم الهاتف بـ 7 ويتكون من 9 أرقام'
            )
        ]
    )
    job = models.CharField(max_length=100, blank=True, null=True, verbose_name="المهنة")
    workplace = models.CharField(max_length=200, blank=True, null=True, verbose_name="جهة العمل")
    education_level = models.CharField(max_length=50, verbose_name="المستوى التعليمي")
    marital_status = models.CharField(
        max_length=20, 
        choices=MARITAL_STATUS, 
        verbose_name="الحالة الاجتماعية"
    )

    def __str__(self):
        return f"{self.full_name} (رقم: {self.victim_id})"

    class Meta:
        unique_together = ('full_name', 'age', 'phone')  # منع التكرار بناء على هذه الحقول
        verbose_name = "مجني عليه"
        verbose_name_plural = "المجني عليهم"
        ordering = ['-victim_id']