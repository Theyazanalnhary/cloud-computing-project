# donors/admin.py
from django.contrib import admin
from .models import Donor

@admin.register(Donor)
class DonorAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'blood_type', 'health_status', 'last_donation_date')
    search_fields = ('full_name', 'blood_type')
    list_filter = ('blood_type', 'health_status')
