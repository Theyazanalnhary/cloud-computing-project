from django.contrib import admin

# Register your models here.
# admin.py
from django.contrib import admin
from .models import Log

# تسجيل النموذج في الإدارة
@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ('log_id', 'employee_id', 'action', 'action_date')
    search_fields = ('employee_id', 'action')
    list_filter = ('action_date',)
