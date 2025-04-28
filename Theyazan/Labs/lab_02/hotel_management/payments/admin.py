from django.contrib import admin
from .models import Payment  # استيراد النموذج من models.py

# تخصيص نموذج Payment في لوحة الإدارة
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['payment_id', 'reservation', 'payment_date', 'amount_paid', 'payment_method']
    search_fields = ['payment_id', 'reservation__customer__first_name', 'payment_method']
    list_filter = ['payment_date', 'payment_method']

# تسجيل النموذج مع تخصيصات الإدارة
admin.site.register(Payment, PaymentAdmin)
