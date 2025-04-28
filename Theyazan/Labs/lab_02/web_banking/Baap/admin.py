from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Blood_Group, Donation, Request

# تسجيل النماذج
@admin.register(Blood_Group)
class BloodGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'date_created', 'date_updated')
    search_fields = ('name',)
    list_filter = ('status',)

@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ('donor_name', 'blood_group', 'donor_contact', 'donor_gender', 'transfusion_date', 'donation_volume', 'date_created')
    search_fields = ('donor_name', 'blood_group__name')
    list_filter = ('blood_group', 'donor_gender', 'transfusion_date')

@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ('patient_name', 'blood_group', 'patient_gender', 'volume', 'status', 'date_created')
    search_fields = ('patient_name', 'blood_group__name')
    list_filter = ('blood_group', 'status', 'patient_gender')