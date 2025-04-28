from django.db import models

# نموذج العرض (Offer)
class Offer(models.Model):
    # معرف العرض
    offer_id = models.AutoField(primary_key=True)  # مفتاح أساسي يتم توليده تلقائيًا
    title = models.CharField(max_length=100)  # عنوان العرض
    description = models.TextField()  # وصف العرض
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)  # نسبة الخصم
    start_date = models.DateField()  # تاريخ بداية العرض
    end_date = models.DateField()  # تاريخ نهاية العرض

    # تمثيل النصي للعرض
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Offer"  # الاسم المفرد للكيان
        verbose_name_plural = "Offers"  # الاسم الجمعي للكيان
