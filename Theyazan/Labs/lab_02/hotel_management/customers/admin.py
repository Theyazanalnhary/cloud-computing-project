# admin.py
from django.contrib import admin
from .models import Customer

# تسجيل النموذج في الإدارة
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('customer_id', 'first_name', 'last_name', 'email', 'phone_number', 'registration_date')
    search_fields = ('first_name', 'last_name', 'email')
    list_filter = ('registration_date',)
