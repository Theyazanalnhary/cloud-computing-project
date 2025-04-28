from django.contrib import admin

from User.models import User 
from Donation.models import Donation
from Inventory.models import Inventory
from Patient.models import Patient
from Requests.models import Request
from Log.models import Log 
from Notification.models import Notification
from Laboratory.models import Laboratory
from Donors.models import Donor 
# Register your models here.
# نموذج المرضى
@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'gender', 'blood_type', 'contact_number', 'medical_condition', 'created_at')
    search_fields = ('full_name', 'contact_number', 'medical_condition')
    list_filter = ('gender', 'blood_type')
    ordering = ('-created_at',)