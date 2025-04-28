from django.db import models
from django.utils.translation import gettext_lazy as _

class ContactMessage(models.Model):
    name = models.CharField(_("الاسم"), max_length=100)
    email = models.EmailField(_("البريد الإلكتروني"))
    subject = models.CharField(_("الموضوع"), max_length=200)
    message = models.TextField(_("الرسالة"))
    created_at = models.DateTimeField(_("تاريخ الإرسال"), auto_now_add=True)
    is_read = models.BooleanField(_("تمت القراءة"), default=False)

    def __str__(self):
        return f"{self.subject} - {self.name}"

    class Meta:
        verbose_name = _("رسالة تواصل")
        verbose_name_plural = _("رسائل التواصل")
