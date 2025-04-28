from django.db import models

# نموذج المخزون (Inventory)
class Inventory(models.Model):
    # معرف العنصر في المخزون
    inventory_id = models.AutoField(primary_key=True)  # مفتاح أساسي يتم توليده تلقائيًا
    item_name = models.CharField(max_length=100)  # اسم العنصر
    quantity = models.IntegerField()  # الكمية المتوفرة
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)  # سعر الوحدة

    # تمثيل النصي للمخزون
    def __str__(self):
        return self.item_name

    class Meta:
        verbose_name = "Inventory"  # الاسم المفرد للكيان
        verbose_name_plural = "Inventories"  # الاسم الجمعي للكيان
