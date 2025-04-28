from django.db import models

# Create your models here.
from django.db import models
from students.models import Student

class Account(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    amount_due = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()

    def __str__(self):
        return f"Account for {self.student}: {self.amount_due}"
