# blood_donation/admin.py
from django.contrib import admin
from .models import Donor

class DonorAdmin(admin.ModelAdmin):
    list_display = ('name', 'blood_type', 'age', 'contact_number', 'donation_date', 'expiration_date')
    list_filter = ('blood_type', 'age')
    search_fields = ('name', 'contact_number')
    ordering = ('-donation_date',)
    readonly_fields = ('donation_date', 'expiration_date')

admin.site.register(Donor, DonorAdmin)
