
# Register your models here.
# admin.py
from django.contrib import admin
from .models import Offer

# تسجيل النموذج في الإدارة
@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ('offer_id', 'title', 'discount_percentage', 'start_date', 'end_date')
    search_fields = ('title', 'description')  # البحث حسب عنوان العرض والوصف
    list_filter = ('start_date', 'end_date')  # تصنيف حسب تاريخ البداية والنهاية
