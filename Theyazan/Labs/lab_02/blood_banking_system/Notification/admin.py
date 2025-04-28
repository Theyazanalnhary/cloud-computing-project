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
# نموذج الإشعارات
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipient', 'message', 'is_read', 'created_at')
    search_fields = ('recipient__username', 'message')
    list_filter = ('is_read',)
    ordering = ('-created_at',)