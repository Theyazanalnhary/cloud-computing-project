from django.contrib import admin

# Register your models here.
# admin.py
from django.contrib import admin
from .models import Notification

# تسجيل النموذج في الإدارة
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('notification_id', 'customer', 'message', 'sent_date', 'is_read')
    search_fields = ('customer__first_name', 'customer__last_name', 'message')  # البحث حسب اسم العميل والمحتوى
    list_filter = ('is_read', 'sent_date')  # تصنيف حسب حالة القراءة وتاريخ الإرسال
