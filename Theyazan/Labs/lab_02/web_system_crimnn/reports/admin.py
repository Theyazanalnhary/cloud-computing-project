from django.contrib import admin
from .models import Report, ReportUpdate

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'reporter', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('title', 'description', 'reporter__username')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

@admin.register(ReportUpdate)
class ReportUpdateAdmin(admin.ModelAdmin):
    list_display = ('report', 'status', 'created_by', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('report__title', 'notes', 'created_by__username')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
