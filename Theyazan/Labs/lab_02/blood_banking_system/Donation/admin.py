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
# نموذج التبرعات
@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ('id', 'donor', 'donation_date', 'blood_type', 'volume_in_ml', 'status', 'processed_by')
    search_fields = ('donor__full_name', 'donation_date', 'blood_type')
    list_filter = ('status', 'blood_type')
    ordering = ('-donation_date',)