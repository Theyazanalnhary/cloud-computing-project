from django.contrib import admin

# Register your models here.
# admin.py
from django.contrib import admin
from .models import Report

# تسجيل النموذج في الإدارة
@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('report_id', 'title', 'created_by', 'created_date', 'content')
    search_fields = ('title', 'content')  # البحث حسب عنوان التقرير ومحتواه
    list_filter = ('created_date',)  # تصنيف حسب تاريخ الإنشاء
