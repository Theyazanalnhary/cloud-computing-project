from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from crimes.models import Crime  # تأكد من أن هذا الاستيراد صحيح
from suspects.models import Suspect
 # أو من التطبيق الصحيح
class Investigation(models.Model):
    """
    نموذج يمثل إجراءات التحقيق في الجريمة
    يحتوي على تفاصيل التحقيق والتواريخ المهمة
    """
    
    # خيارات حالة التحقيق
    STATUS_CHOICES = [
        ('مقبوض', 'مقبوض'),
        ('هارب', 'هارب')
    ]
    
    # رقم الإجراء (مفتاح أساسي)
    investigation_id = models.AutoField(primary_key=True, verbose_name="رقم الإجراء")
    
   # تعديل العلاقة مع الجريمة لتعكس التغيير في النموذج
    crime = models.ForeignKey(
        Crime, 
        on_delete=models.CASCADE, 
        verbose_name="الجريمة",
        related_name="investigations"
    )
    
    # تعديل العلاقة مع المتهم لتعكس التغيير في النموذج
    suspect = models.ForeignKey(
        Suspect,
        on_delete=models.CASCADE,
        verbose_name="المتهم",
        related_name="investigations"
    )
    
    # ========== حالة التحقيق ==========
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default='مقبوض',
        verbose_name="حالة التحقيق"
    )
    
    # ========== تواريخ التحقيق ==========
    arrest_date = models.DateTimeField(null=True, blank=True, verbose_name="تاريخ القبض")
    detention_date = models.DateField(null=True, blank=True, verbose_name="تاريخ التوقيف")
    release_date = models.DateField(null=True, blank=True, verbose_name="تاريخ الإفراج")
    transfer_date = models.DateField(null=True, blank=True, verbose_name="تاريخ النقل")
    
    # ========== تفاصيل التحقيق ==========
    arrest_method = models.TextField(blank=True, null=True, verbose_name="كيفية القبض")
    arresting_officer = models.CharField(max_length=100, blank=True, null=True, verbose_name="ضابط القبض")
    transferred_to = models.CharField(max_length=100, blank=True, null=True, verbose_name="نقل إلى")
    
    # ========== معلومات الإفراج ==========
    released_on_bail = models.BooleanField(default=False, verbose_name="إفراج بضمان؟")
    bail_guarantor = models.CharField(max_length=100, blank=True, null=True, verbose_name="اسم الضامن")
    
    # ========== حالة القضية ==========
    case_closed = models.BooleanField(default=False, verbose_name="انتهت القضية؟")
    procedure_stopped = models.BooleanField(default=False, verbose_name="وقف الإجراءات؟")
    referred_to = models.CharField(max_length=100, blank=True, null=True, verbose_name="الإحالة إلى")
    issuing_authority = models.CharField(max_length=100, blank=True, null=True, verbose_name="السلطة الآمرة")

    def clean(self):
        """
        التحقق من صحة البيانات قبل الحفظ
        """
        errors = {}
        
        # التحقق من أن تاريخ الإفراج ليس قبل تاريخ التوقيف
        if self.release_date and self.detention_date and self.release_date < self.detention_date:
            errors['release_date'] = "تاريخ الإفراج لا يمكن أن يكون قبل تاريخ التوقيف"
        
        # التحقق من أن تاريخ القبض ليس في المستقبل
        if self.arrest_date and self.arrest_date > timezone.now():
            errors['arrest_date'] = "تاريخ القبض لا يمكن أن يكون في المستقبل"
        
        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        """
        حفظ النموذج مع تحديث الحالة تلقائياً من حالة المتهم
        """
        # تحديث حالة التحقيق بناءً على حقل is_fugitive في المتهم
        if self.suspect.is_fugitive:
            self.status = 'هارب'
        else:
            self.status = 'مقبوض'
            
        # التحقق من صحة البيانات قبل الحفظ
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        """
        تمثيل نصي لإجراء التحقيق
        """
        return f"تحقيق #{self.investigation_id} - {self.suspect.full_name} ({self.status})"

    class Meta:
        """
        بيانات تعريفية عن النموذج
        """
        # ضمان عدم تكرار التحقيقات لنفس المتهم في نفس الجريمة
        unique_together = ('crime', 'suspect')
        verbose_name = "إجراء تحري"
        verbose_name_plural = "إجراءات التحري"
        ordering = ['-arrest_date']  # ترتيب حسب تاريخ القبض تنازلياً