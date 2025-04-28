from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class CrimeType(models.Model):
    name = models.CharField(_("نوع الجريمة"), max_length=100)
    description = models.TextField(_("الوصف"), blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("نوع الجريمة")
        verbose_name_plural = _("أنواع الجرائم")

class Report(models.Model):
    STATUS_CHOICES = (
        ('new', 'جديد'),
        ('in_progress', 'قيد المعالجة'),
        ('under_investigation', 'قيد التحقيق'),
        ('resolved', 'تم الحل'),
        ('closed', 'مغلق'),
    )

    title = models.CharField(_("عنوان البلاغ",),default="Usss", max_length=200)
    description = models.TextField(_("وصف البلاغ"))
    location = models.CharField(_("الموقع"), max_length=255)
    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reports',
        verbose_name=_("المبلغ")
    )
    status = models.CharField(
        _("الحالة"),
        max_length=20,
        choices=STATUS_CHOICES,
        default='new'
    )
    created_at = models.DateTimeField(_("تاريخ الإنشاء"), auto_now_add=True)
    updated_at = models.DateTimeField(_("تاريخ التحديث"), auto_now=True)
    
    # ملفات مرفقة (اختياري)
    attachment = models.FileField(
        _("مرفقات"),
        upload_to='reports/attachments/',
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = _("بلاغ")
        verbose_name_plural = _("البلاغات")
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class ReportUpdate(models.Model):
    STATUS_CHOICES = (
        ('in_progress', 'قيد المعالجة'),
        ('under_investigation', 'قيد التحقيق'),
        ('resolved', 'تم الحل'),
        ('closed', 'مغلق'),
    )

    report = models.ForeignKey(
        Report,
        on_delete=models.CASCADE,
        related_name='updates',
        verbose_name=_("البلاغ")
    )
    status = models.CharField(
        _("الحالة"),
        max_length=20,
        choices=STATUS_CHOICES
    )
    notes = models.TextField(_("ملاحظات"))
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='report_updates',
        verbose_name=_("تم التحديث بواسطة")
    )
    created_at = models.DateTimeField(_("تاريخ التحديث"), auto_now_add=True)
    
    # ملفات مرفقة (اختياري)
    attachment = models.FileField(
        _("مرفقات"),
        upload_to='reports/updates/attachments/',
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = _("تحديث البلاغ")
        verbose_name_plural = _("تحديثات البلاغات")
        ordering = ['-created_at']

    def __str__(self):
        return f"تحديث لبلاغ: {self.report.title}"

    def save(self, *args, **kwargs):
        # تحديث حالة البلاغ الرئيسي
        self.report.status = self.status
        self.report.save()
        super().save(*args, **kwargs)

class ReportMedia(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='media')
    file = models.FileField(_("الملف"), upload_to='reports/')
    file_type = models.CharField(_("نوع الملف"), max_length=10)
    uploaded_at = models.DateTimeField(_("تاريخ الرفع"), auto_now_add=True)

    class Meta:
        verbose_name = _("ملف مرفق")
        verbose_name_plural = _("الملفات المرفقة")
