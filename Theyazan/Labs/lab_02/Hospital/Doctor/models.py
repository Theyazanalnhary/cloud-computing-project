from django.db import models

class Doctor(models.Model):
    # الحقول الأساسية
    firstD_name = models.CharField(max_length=100, default='Unkown')
    lastD_name = models.CharField(max_length=100, default='Unkown')
    age = models.PositiveIntegerField(default=30)
    specialization = models.CharField(max_length=100, default='General')
    
    image = models.ImageField(upload_to='doctor_images/%y/%m/%d', null=True)
    file_report = models.FileField(upload_to='doctor_files/%y/%m/%d', null=True)
    upload_at = models.DateTimeField(auto_now_add=True, null=True)
    bio = models.TextField(max_length=500, default='Biography not provided')

    def __str__(self):
        return f"{self.firstD_name} {self.lastD_name}"
