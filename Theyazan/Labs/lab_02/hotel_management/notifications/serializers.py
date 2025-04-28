# serializers.py
from rest_framework import serializers
from .models import Notification
from customers.models import Customer  # استيراد نموذج العميل

class NotificationSerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())  # ربط العميل بالإشعار

    class Meta:
        model = Notification
        fields = ['notification_id', 'customer', 'message', 'sent_date', 'is_read']  # تضمين الحقول المطلوبة
