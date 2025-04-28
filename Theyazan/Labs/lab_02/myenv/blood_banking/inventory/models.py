# inventory/models.py

from django.db import models

class InventoryItem(models.Model):
    blood_type = models.CharField(max_length=3)
    quantity = models.IntegerField()  # الكمية المتوفرة في المخزون
    expiration_date = models.DateField()

    def __str__(self):
        return f'{self.blood_type} - {self.quantity} units'
