from django.db import models
from django.core.exceptions import ValidationError
from crimes.models import Crime
from django.core.validators import RegexValidator
from django.core.validators import MinValueValidator, MaxValueValidator  # <-- أضف هذا الاستيراد


class Suspect(models.Model):
    """
    نموذج يمثل المتهم في النظام
    يحتوي على المعلومات الشخصية وتفاصيل الاتصال والمعلومات المتعلقة بالجريمة
    """

      # خيارات الجنس
    GENDER_CHOICES = [('ذكر', 'ذكر'), ('أنثى', 'أنثى')]
    
    # خيارات الحالة الاجتماعية
    MARITAL_STATUS = [('أعزب', 'أعزب'), ('متزوج', 'متزوج')]
    
    # رقم المتهم (مفتاح أساسي)
    suspect_id = models.AutoField(primary_key=True, verbose_name="رقم المتهم")
    
     # علاقة ManyToMany مع الجرائم (بدلاً من ForeignKey)
    crimes = models.ManyToManyField(
        Crime, 
        related_name="suspects",
        verbose_name="الجرائم المرتبطة"
    )
    
    # ========== المعلومات الشخصية ==========
    full_name = models.CharField(max_length=100, verbose_name="الاسم الثلاثي")
    nickname = models.CharField(max_length=50, blank=True, null=True, verbose_name="اللقب")
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, verbose_name="الجنس")
    nationality = models.CharField(max_length=50, verbose_name="الجنسية")
    country = models.CharField(max_length=50, verbose_name="البلد")

    # العمر مع تحقق من المدى (7-120 سنة)
    age = models.PositiveIntegerField(verbose_name="العمر", validators=[
        MinValueValidator(7),  # <-- تم التصحيح هنا
        MaxValueValidator(120)  # <-- تم التصحيح هنا
    ])
    
    # ========== معلومات الاتصال ==========
    phone = models.CharField(
        max_length=20, 
        blank=True, 
        null=True, 
        verbose_name="رقم الهاتف",
        validators=[RegexValidator(regex='^[0-9]+$', message='يجب أن يحتوي على أرقام فقط')]
    )
    residence = models.CharField(max_length=200, verbose_name="محل الإقامة")
    
    # ========== معلومات العمل ==========
    job = models.CharField(max_length=100, blank=True, null=True, verbose_name="المهنة")
    workplace = models.CharField(max_length=200, blank=True, null=True, verbose_name="جهة العمل")
    
    # ========== معلومات إضافية ==========
    marital_status = models.CharField(max_length=20, choices=MARITAL_STATUS, 
                                     verbose_name="الحالة الاجتماعية")
    education_level = models.CharField(max_length=50, verbose_name="المستوى التعليمي")
    relationship_with_victim = models.CharField(max_length=100, blank=True, 
                                              null=True, verbose_name="علاقة بالمجني عليه")
    
    # ========== معلومات الجريمة ==========
    role_in_crime = models.TextField(verbose_name="دور في الجريمة")
    
    # الجرائم السابقة (علاقة متعددة مع نموذج الجريمة)
    previous_crimes = models.ManyToManyField(Crime, related_name="related_suspects", 
                                           blank=True, verbose_name="الجرائم السابقة")
    
    # ========== معلومات تقنية ==========
    face_encoding = models.JSONField(blank=True, null=True, verbose_name="بصمة الوجه")
    
    # ========== حالة المتهم ==========
    is_fugitive = models.BooleanField(
        default=False,
        verbose_name="هارب؟",
        help_text="إذا تم اختياره يعني المتهم هارب، وإلا يعتبر مقبوض"
    )
    
    # ========== تواريخ مهمة ==========
# تغيير اسم الحقل
    preventive_detention_date = models.DateField(blank=True, null=True, verbose_name="تاريخ الحبس الاحتياطي")
    release_date = models.DateField(blank=True, null=True, verbose_name="تاريخ الإفراج")
    
    def clean(self):
        """
        التحقق من صحة البيانات قبل الحفظ
        """
        if self.preventive_detention_date and self.release_date and self.release_date < self.preventive_detention_date:
            raise ValidationError("تاريخ الإفراج لا يمكن أن يكون قبل تاريخ التوقيف")
    
    def __str__(self):
        """
        تمثيل نصي للمتهم
        """
        return f"{self.full_name} (رقم: {self.suspect_id})"
    
    class Meta:
        """
        بيانات تعريفية عن النموذج
        """
        # ضمان عدم تكرار المتهمين بنفس البيانات الأساسية
        unique_together = ('full_name', 'age', 'phone')
        verbose_name = "متهم"
        verbose_name_plural = "المتهمون"
        ordering = ['-suspect_id']  # ترتيب حسب رقم المتهم تنازلياً


