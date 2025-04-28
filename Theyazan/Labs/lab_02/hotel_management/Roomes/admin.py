from django.contrib import admin
from django.utils.html import format_html
from .models import Room

class RoomAdmin(admin.ModelAdmin):
    # عرض الأعمدة في القائمة
    list_display = ('room_number', 'room_type', 'number_of_rooms', 'price_per_night', 'status', 'capacity', 'room_image_display')  
    
    # تصفية البيانات في القائمة حسب نوع الغرفة والحالة والسعة
    list_filter = ('room_type', 'status', 'capacity')  
    
    # البحث في الأعمدة المذكورة
    search_fields = ('room_number', 'room_type', 'description')  
    
    # ترتيب الغرف حسب الرقم
    ordering = ('room_number',)  
    
    # دالة لعرض الصورة في واجهة الإدارة
    def room_image_display(self, obj):
        if obj.room_image:
            return format_html('<img src="{}" width="100" height="100" />', obj.room_image.url)
        return 'لا توجد صورة'
    room_image_display.short_description = 'الصورة'  # تعيين اسم العمود في واجهة الإدارة

# تسجيل نموذج Room في لوحة الإدارة
admin.site.register(Room, RoomAdmin)
