from django.db import models
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

class User(models.Model):
    ROLE_CHOICES = [
        ('admin', 'مدير'),
        ('user', 'مستخدم عادي'),
    ]

    # FIELDS
    userid = models.AutoField(primary_key=True)
    fname = models.CharField(max_length=25, verbose_name='الاسم الأول')
    sname = models.CharField(max_length=25, verbose_name='الاسم الأخير')
    loginname = models.CharField(max_length=15, unique=True, verbose_name='اسم المستخدم')
    password = models.CharField(max_length=128, verbose_name='كلمة المرور')
    phone = models.BigIntegerField(
        null=True, blank=True, verbose_name='الهاتف',
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message='رقم الهاتف غير صالح')]
    )
    email = models.EmailField(max_length=65, null=True, blank=True, unique=True, verbose_name='البريد الإلكتروني')
    country = models.CharField(max_length=50, null=True, blank=True, verbose_name='البلد')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user', verbose_name='الدور')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاريخ التعديل')

    # METHODS

    def save(self, *args, **kwargs):
        if self.password:
            self.password = make_password(self.password)  # Encrypt the password before saving
        super(User, self).save(*args, **kwargs)

    def clean(self):
        # Validate password length
        if len(self.password) < 8:
            raise ValidationError('كلمة المرور يجب أن تكون على الأقل 8 حروف.')
        super().clean()

    def is_admin(self):
        return self.role == 'admin'

    def is_user(self):
        return self.role == 'user'

    # STRING REPRESENTATION
    def __str__(self):
        return f"{self.fname} {self.sname} ({self.loginname})"

    class Meta:
        verbose_name = 'مستخدم'
        verbose_name_plural = 'المستخدمين'
        indexes = [
            models.Index(fields=['loginname']),
            models.Index(fields=['email']),
        ]
