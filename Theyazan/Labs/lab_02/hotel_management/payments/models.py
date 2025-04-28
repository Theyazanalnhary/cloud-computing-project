from django.db import models
from customers.models import Customer
from reservations.models import Reservation

# نموذج الدفع
class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)  # ربط الحجز
    payment_date = models.DateTimeField()
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)  # المبلغ المدفوع
    remaining_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # المبلغ المتبقي
    payment_method = models.CharField(
        max_length=50,
        choices=[
            ('cash', 'كاش'),
            ('credit_card', 'بطاقة ائتمان'),
            ('bank_transfer', 'تحويل بنكي'),
            ('other', 'أخرى'),
        ]
    )
    payment_reference = models.CharField(max_length=100, null=True, blank=True)  # الرقم المرجعي للعملية
    card_number = models.CharField(max_length=50, null=True, blank=True)  # رقم البطاقة (اختياري)

    # دالة الحفظ لحساب المبلغ المتبقي
    def save(self, *args, **kwargs):
        # التحقق من وجود الحجز والمبلغ الإجمالي قبل الحفظ
        if self.reservation and hasattr(self.reservation, 'total_amount'):
            total_amount = self.reservation.total_amount or 0

            # التحقق من أن المبلغ المدفوع لا يتجاوز المبلغ الإجمالي
            if self.amount_paid > total_amount:
                raise ValueError("المبلغ المدفوع لا يمكن أن يكون أكبر من المبلغ الإجمالي")

            # حساب المبلغ المتبقي
            self.remaining_amount = total_amount - self.amount_paid
        else:
            # في حال عدم تحديد الحجز، يتم اعتبار المبلغ المتبقي يساوي المدفوع
            self.remaining_amount = self.amount_paid

        # استدعاء الحفظ الأساسي
        super(Payment, self).save(*args, **kwargs)

    # النص التوضيحي للكائن
    def __str__(self):
        return f"Payment {self.payment_id}"

    # إعدادات العرض في لوحة الإدارة
    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"
