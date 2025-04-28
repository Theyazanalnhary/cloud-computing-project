# blood_units/models.py
from django.db import models
from donors.models import Donor

class BloodUnit(models.Model):
    STATUS_CHOICES = [('available', 'Available'), ('used', 'Used'), ('expired', 'Expired'), ('reserved', 'Reserved')]
    BLOOD_TYPE_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE)
    blood_type = models.CharField(max_length=3,choices=BLOOD_TYPE_CHOICES)
    donation_date = models.DateField()
    expiry_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    quantity = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"Unit {self.id} - {self.blood_type}"
