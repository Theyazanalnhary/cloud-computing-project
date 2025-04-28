from django.contrib import admin

# Register your models here.
# admin.py
from django.contrib import admin
from .models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ['fname', 'sname', 'loginname', 'email', 'role', 'created_at', 'updated_at']
    search_fields = ['loginname', 'email']
    list_filter = ['role']
    ordering = ['created_at']
    
admin.site.register(User, UserAdmin)
