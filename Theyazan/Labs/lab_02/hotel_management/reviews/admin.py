# admin.py
from django.contrib import admin
from .models import Review

# تسجيل النموذج في الإدارة
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('review_id', 'customer', 'room', 'rating', 'review_date')  # عرض الأعمدة في لوحة الإدارة
    search_fields = ('customer__first_name', 'room__room_number', 'rating')  # البحث حسب اسم العميل ورقم الغرفة والتقييم
    list_filter = ('rating', 'review_date')  # تصنيف حسب التقييم وتاريخ التقييم
