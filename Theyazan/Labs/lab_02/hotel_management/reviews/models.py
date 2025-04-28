from django.db import models
from customers.models import Customer
from Roomes.models import Room



# نموذج التقييم (Review)
class Review(models.Model):
    # معرف التقييم
    review_id = models.AutoField(primary_key=True)  # مفتاح أساسي يتم توليده تلقائيًا
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)  # مفتاح خارجي يشير إلى العميل (علاقة مع نموذج Customer)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)  # مفتاح خارجي يشير إلى الغرفة (علاقة مع نموذج Room)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # التقييم (من 1 إلى 5)
    comments = models.TextField()  # التعليقات
    review_date = models.DateTimeField()  # تاريخ التقييم

    # تمثيل النصي للتقييم
    def __str__(self):
        return f"Review {self.review_id}"

    class Meta:
        verbose_name = "Review"  # الاسم المفرد للكيان
        verbose_name_plural = "Reviews"  # الاسم الجمعي للكيان

