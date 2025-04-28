from django.db import models

class Recipient(models.Model):
    name = models.CharField(max_length=100)
    blood_type = models.CharField(max_length=3)
    age = models.IntegerField(blank=True, null=True)  # يمكن تركه فارغاً
    request_date = models.DateTimeField(blank=True, null=True)  # يمكن تركه فارغاً
    quantity = models.IntegerField(blank=True, null=True)  # يمكن تركه فارغاً

    def __str__(self):
        return self.name
