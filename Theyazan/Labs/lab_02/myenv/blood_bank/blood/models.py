from django.db import models
from datetime import timedelta
from django.utils import timezone

class Donor(models.Model):
    BLOOD_TYPES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
    ]

    name = models.CharField(max_length=100)
    blood_type = models.CharField(max_length=3, choices=BLOOD_TYPES, db_index=True)
    age = models.IntegerField()
    contact_number = models.CharField(max_length=15)
    donation_date = models.DateTimeField(auto_now_add=True)
    expiration_date = models.DateTimeField(blank=True, null=True)
    quantity = models.IntegerField(default=0)  # الكمية المتاحة لكل فصيلة

    def save(self, *args, **kwargs):
        if self.donation_date and not self.expiration_date:
            self.expiration_date = self.donation_date + timedelta(days=30)
        super(Donor, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.name} - {self.blood_type} - {self.quantity}'
