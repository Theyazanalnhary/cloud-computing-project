from django.contrib import admin

# Register your models here.
# admin.py
from django.contrib import admin
from .models import Inventory

# تسجيل النموذج في الإدارة
@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('inventory_id', 'item_name', 'quantity', 'unit_price')
    search_fields = ('item_name',)
    list_filter = ('quantity',)
