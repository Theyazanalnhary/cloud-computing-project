from django.db import models
from django.conf import settings

class CrimeReport(models.Model):
    STATUS_CHOICES = (
        ('new', 'جديد'),
        ('under_investigation', 'قيد التحقيق'),
        ('solved', 'تم الحل'),
        ('closed', 'مغلق'),
    )
    
    PRIORITY_CHOICES = (
        ('high', 'عالية'),
        ('medium', 'متوسطة'),
        ('low', 'منخفضة'),
    )
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    date_occurred = models.DateTimeField()
    date_reported = models.DateTimeField(auto_now_add=True)
    
    reporter_name = models.CharField(max_length=100)
    reporter_phone = models.CharField(max_length=20)
    reporter_email = models.EmailField()
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_reports'
    )
    
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    def __str__(self):
        return f"{self.title} - {self.get_status_display()}"

class Evidence(models.Model):
    report = models.ForeignKey(CrimeReport, on_delete=models.CASCADE, related_name='evidences')
    title = models.CharField(max_length=100)
    description = models.TextField()
    file = models.FileField(upload_to='evidences/')
    date_added = models.DateTimeField(auto_now_add=True)
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

class Investigation(models.Model):
    report = models.ForeignKey(CrimeReport, on_delete=models.CASCADE, related_name='investigations')
    investigator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    notes = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True) 