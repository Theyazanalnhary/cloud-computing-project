from django.db import models

class Room(models.Model):
    # أنواع الغرف
    ROLE_CHOICES = [
        ('single', 'فردية'),
        ('double', 'مزدوجة'),
        ('family', 'عائلية'),
        ('apartment', 'شقة'),
        ('suite', 'جناح'),
    ]
    
    # اختيار حالة الغرفة
    STATUS_CHOICES = [
        ('available', 'متاحة'),
        ('booked', 'محجوزة'),
        ('maintenance', 'صيانة'),
    ]

    # اختيار السعة (عدد الأشخاص)
    CAPACITY_CHOICES = [
        (1, '1 شخص'),
        (2, '2 أشخاص'),
        (3, '3 أشخاص'),
        (4, '4 أشخاص'),
        (5, '5 أشخاص'),
    ]

    # الحقول الأساسية
    room_id = models.AutoField(primary_key=True)  # مفتاح أساسي يتم توليده تلقائيًا
    room_number = models.CharField(max_length=10, unique=True)  # رقم الغرفة مع التأكد من التفرد
    room_type = models.CharField(max_length=50, choices=ROLE_CHOICES)  # نوع الغرفة
    number_of_rooms = models.IntegerField()  # عدد الغرف المتاحة لهذا النوع
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)  # السعر لكل ليلة
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)  # حالة الغرفة
    description = models.TextField()  # وصف الغرفة
    capacity = models.IntegerField(choices=CAPACITY_CHOICES)  # السعة (عدد الأشخاص)
    
    # تعديل الحقل لتخزين الصورة بدلاً من الرابط
    room_image = models.ImageField(upload_to='room_images/', blank=True, null=True)  # مسار تخزين الصور

    def __str__(self):
        return f"Room {self.room_number} ({self.room_type})"
     # وظيفة لتقليل عدد الغرف المتاحة عند الحجز
    def book_room(self):
        if self.number_of_rooms > 0:
            self.number_of_rooms -= 1
            self.save()
        else:
            raise ValueError("لا توجد غرف متاحة لهذا النوع")
            
    class Meta:
        verbose_name = "غرفة"
        verbose_name_plural = "غرف"
