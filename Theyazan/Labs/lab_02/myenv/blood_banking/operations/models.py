from django.db import models

class Operation(models.Model):
    OPERATION_TYPES = [
        ('donation', 'متبرع'),
        ('distribution', 'توزيع'),
    ]

    operation_name = models.CharField(max_length=100)
    operation_date = models.DateField()
    operation_type = models.CharField(max_length=100, choices=OPERATION_TYPES,blank=True,null=True)  # إضافة نوع العملية

    def __str__(self):
        return f"{self.operation_name} - {self.operation_type}"
