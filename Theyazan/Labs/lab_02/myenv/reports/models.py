from django.db import models
from django.conf import settings

class CrimeReport(models.Model):
    CRIME_TYPES = [
        ('theft', 'سرقة'),
        ('assault', 'اعتداء'),
        ('murder', 'قتل'),
        ('other', 'أخرى'),
    ]

    STATUS_CHOICES = [
        ('pending', 'قيد المراجعة'),
        ('investigating', 'قيد التحقيق'),
        ('closed', 'مغلق'),
    ]

    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reports'
    )
    crime_type = models.CharField(max_length=20, choices=CRIME_TYPES)
    location = models.CharField(max_length=255)
    description = models.TextField()
    date_reported = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    reference_number = models.CharField(max_length=20, unique=True)
    is_anonymous = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.reference_number:
            # Generate unique reference number
            import random
            import string
            while True:
                ref = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
                if not CrimeReport.objects.filter(reference_number=ref).exists():
                    self.reference_number = ref
                    break
        super().save(*args, **kwargs)

class ReportImage(models.Model):
    report = models.ForeignKey(CrimeReport, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='report_images/') 