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
# نموذج المخزون
@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'blood_type', 'quantity_in_ml', 'expiry_date', 'status')
    search_fields = ('blood_type', 'status')
    list_filter = ('status', 'blood_type')
    ordering = ('-expiry_date',)