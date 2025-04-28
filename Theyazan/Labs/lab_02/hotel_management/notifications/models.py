from django.db import models
from customers.models import Customer


# نموذج الإشعار (Notification)
class Notification(models.Model):
    # معرف الإشعار
    notification_id = models.AutoField(primary_key=True)  # مفتاح أساسي يتم توليده تلقائيًا
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)  # مفتاح خارجي يشير إلى العميل (علاقة مع نموذج Customer)
    message = models.TextField()  # محتوى الإشعار
    sent_date = models.DateTimeField()  # تاريخ إرسال الإشعار
    is_read = models.BooleanField(default=False)  # هل تم قراءة الإشعار (افتراضيًا لا)

    # تمثيل النصي للإشعار
    def __str__(self):
        return f"Notification {self.notification_id}"

    class Meta:
        verbose_name = "Notification"  # الاسم المفرد للكيان
        verbose_name_plural = "Notifications"  # الاسم الجمعي للكيان

