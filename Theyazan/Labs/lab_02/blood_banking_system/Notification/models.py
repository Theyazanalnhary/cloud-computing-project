from django.db import models
from User.models import User
# Create your models here.
# جدول الإشعارات
class Notification(models.Model):
    # تعريف الحقول
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')  # المستلم
    message = models.TextField()  # الرسالة النصية للإشعار
    is_read = models.BooleanField(default=False)  # حالة القراءة (قراءة أو غير قراءة)
    created_at = models.DateTimeField(auto_now_add=True)  # وقت إرسال الإشعار
    
    def __str__(self):
        return f"Notification for {self.recipient.username} on {self.created_at}"

