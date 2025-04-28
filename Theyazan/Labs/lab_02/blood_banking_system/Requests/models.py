from django.db import models
from Patient.models import Patient
from Donors.models import Donor
from User.models import User
# Create your models here.
# جدول الطلبات
class Request(models.Model):
    # خيارات حالة الطلب
    STATUS_CHOICES = [
        ('Pending', 'قيد الانتظار'),
        ('Approved', 'تمت الموافقة'),
        ('Rejected', 'مرفوض'),
        ('Completed', 'مكتمل'),
    ]
    
    # تعريف الحقول
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='requests')  # المريض الذي قام بتقديم الطلب
    blood_type = models.CharField(max_length=3, choices=Donor.BLOOD_TYPES)  # فصيلة الدم المطلوبة
    quantity_in_ml = models.PositiveIntegerField()  # كمية الدم المطلوبة بالملليتر
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)  # حالة الطلب
    requested_by = models.ForeignKey(User, related_name='requests_created', on_delete=models.SET_NULL, null=True)  # الموظف الذي سجل الطلب
    processed_by = models.ForeignKey(User, related_name='requests_processed', on_delete=models.SET_NULL, null=True, blank=True)  # الموظف الذي عالج الطلب
    request_date = models.DateTimeField(auto_now_add=True)  # تاريخ طلب الدم

    def __str__(self):
        return f"Request for {self.blood_type} ({self.quantity_in_ml} ml)"

