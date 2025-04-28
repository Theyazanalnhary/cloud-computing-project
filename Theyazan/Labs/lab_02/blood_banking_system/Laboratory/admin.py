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
# نموذج المختبرات
@admin.register(Laboratory)
class LaboratoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'location', 'contact_number', 'created_at')
    search_fields = ('name', 'location')
    ordering = ('-created_at',)