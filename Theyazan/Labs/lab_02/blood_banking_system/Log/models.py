from django.db import models
from User.models import User
# Create your models here.
# جدول السجلات
class Log(models.Model):
    # تعريف الحقول
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='logs')  # المستخدم الذي قام بالإجراء
    action = models.CharField(max_length=255)  # الإجراء المتخذ
    timestamp = models.DateTimeField(auto_now_add=True)  # وقت إجراء العملية
    
    def __str__(self):
        return f"Log by {self.user.username} at {self.timestamp}"
