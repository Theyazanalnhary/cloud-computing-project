# admin.py
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
# تخصيص واجهة المستخدم للموديلات

# نموذج المستخدمين
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'full_name', 'role', 'email', 'phone_number', 'created_at')
    search_fields = ('username', 'email', 'full_name')
    list_filter = ('role',)
    ordering = ('-created_at',)