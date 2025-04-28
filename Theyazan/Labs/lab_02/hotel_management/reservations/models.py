from django.db import models
from Roomes.models import Room
from django.db.models import Q  # استيراد Q للبحث بشروط متعددة
from customers.models import Customer

# نموذج الحجز (Reservation)

class Reservation(models.Model):
    # معرف الحجز
    reservation_id = models.AutoField(primary_key=True)  # مفتاح أساسي يتم توليده تلقائيًا
    room = models.ForeignKey(Room, related_name="reservations", on_delete=models.CASCADE)  # مفتاح خارجي    
    # الحقول الجديدة

    customer_id = models.ForeignKey(Customer ,on_delete=models.CASCADE, null=True)

    number_of_rooms = models.PositiveIntegerField(default=1)  # عدد الغرف المطلوبة
    check_in_date = models.DateTimeField()  # تاريخ ووقت الدخول
    check_out_date = models.DateTimeField()  # تاريخ ووقت الخروج
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True)  # المبلغ الإجمالي
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'قيد الانتظار'),
            ('confirmed', 'مؤكد'),
            ('canceled', 'ملغي'),
        ],
        default='pending'
    )  # حالة الحجز

    # تحديث السعر الإجمالي تلقائيًا بناءً على عدد الغرف وسعر الغرفة
    def save(self, *args, **kwargs):
        # التحقق من صحة التواريخ
        if self.check_in_date >= self.check_out_date:
            raise ValueError("تاريخ الدخول يجب أن يكون قبل تاريخ الخروج.")

        # حساب عدد الليالي المحجوزة
        total_days = (self.check_out_date - self.check_in_date).days
        if total_days < 1:
            raise ValueError("مدة الحجز يجب أن تكون يومًا واحدًا على الأقل.")

        # تحقق إذا كانت الغرفة محجوزة بالفعل خلال الفترة المطلوبة
        existing_reservations = Reservation.objects.filter(
            Q(room=self.room) & 
            (
                (Q(check_in_date__lte=self.check_out_date) & Q(check_out_date__gte=self.check_in_date))  # تحقق من التداخل في التواريخ
            )
        )

        if existing_reservations.exists():
            raise ValueError("الغرفة محجوزة بالفعل في هذه الفترة.")

        # حساب السعر الإجمالي بناءً على عدد الغرف وعدد الليالي وسعر الغرفة
        price_per_room = self.room.price_per_night
        total_amount = price_per_room * self.number_of_rooms * total_days
        self.total_amount = total_amount  # تعيين المبلغ الإجمالي

        # استدعاء الحفظ بعد التحديث
        super().save(*args, **kwargs)

    # التمثيل النصي للحجز
    def __str__(self):
        return f"Reservation {self.reservation_id} - {self.number_of_rooms} غرفة/غرف - المبلغ الإجمالي: {self.total_amount}"

    # إعدادات وصفية
    class Meta:
        verbose_name = "Reservation"
        verbose_name_plural = "Reservations"
