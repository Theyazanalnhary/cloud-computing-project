from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

# Create your models here.

class User(AbstractUser):
    ROLE_CHOICES = (
        ('citizen', 'مواطن'),
        ('police', 'شرطة'),
        ('admin', 'مدير نظام'),
    )
    
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name=_('groups'),
        blank=True,
        related_name='custom_user_set',
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name=_('user permissions'),
        blank=True,
        related_name='custom_user_set',
        help_text=_('Specific permissions for this user.'),
    )
    
    phone_number = models.CharField(_("رقم الهاتف"), max_length=20, blank=True)
    role = models.CharField(_("الدور"), max_length=20, choices=ROLE_CHOICES, default='citizen')
    address = models.TextField(_("العنوان"), blank=True)
    created_at = models.DateTimeField(_("تاريخ الإنشاء"), auto_now_add=True)
    updated_at = models.DateTimeField(_("تاريخ التحديث"), auto_now=True)
    
    # حقول إضافية للتسجيل الاجتماعي
    social_id = models.CharField(max_length=100, blank=True, null=True)
    social_provider = models.CharField(max_length=30, blank=True, null=True)
    
    def get_social_avatar(self):
        if self.social_provider == 'facebook':
            return f"https://graph.facebook.com/{self.social_id}/picture?type=large"
        return None

    class Meta:
        verbose_name = _("مستخدم")
        verbose_name_plural = _("المستخدمين")
