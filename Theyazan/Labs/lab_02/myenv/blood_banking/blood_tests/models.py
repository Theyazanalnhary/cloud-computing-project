# blood_tests/models.py
from django.db import models

class User(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.username


class BloodTest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blood_tests', null=True, blank=True)

   # user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blood_tests')
    test_date = models.DateField()
    result = models.CharField(max_length=100)

    def __str__(self):
        return f'Test for {self.user.username} on {self.test_date}'


class Recipient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='recipient')
    blood_type = models.CharField(max_length=3)

    def __str__(self):
        return f'Recipient: {self.user.username}'


class BloodRequest(models.Model):
    recipient = models.ForeignKey(Recipient, on_delete=models.CASCADE, related_name='blood_requests')
    request_date = models.DateField()
    quantity = models.IntegerField()

    def __str__(self):
        return f'Request from {self.recipient.user.username} on {self.request_date}'


class Operation(models.Model):
    recipient = models.ForeignKey(Recipient, on_delete=models.CASCADE, related_name='operations')
    operation_date = models.DateField()
    description = models.TextField()

    def __str__(self):
        return f'Operation for {self.recipient.user.username} on {self.operation_date}'


class Inventory(models.Model):
    blood_type = models.CharField(max_length=3)
    quantity = models.IntegerField()

    def __str__(self):
        return f'Inventory: {self.blood_type} - {self.quantity} units'
