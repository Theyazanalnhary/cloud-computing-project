# blood_requests/serializers.py

from rest_framework import serializers
from .models import BloodRequest
from recipients.models import Recipient  # تأكد من استيراد نموذج المستفيد

class BloodRequestSerializer(serializers.ModelSerializer):
    recipient_name = serializers.CharField(source='recipient.name', read_only=True)

    class Meta:
        model = BloodRequest
        fields = ['id', 'recipient_name', 'blood_type', 'request_date', 'received_status', 'quantity_received', 'status']
