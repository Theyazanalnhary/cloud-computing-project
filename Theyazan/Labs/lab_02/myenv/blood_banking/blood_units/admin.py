# blood_units/admin.py
from django.contrib import admin
from .models import BloodUnit

@admin.register(BloodUnit)
class BloodUnitAdmin(admin.ModelAdmin):
    list_display = ('blood_type', 'donation_date', 'expiry_date', 'status')
    list_filter = ('blood_type', 'status')
