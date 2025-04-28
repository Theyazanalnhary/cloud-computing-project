# serializers.py
from rest_framework import serializers
from .models import Payment
from reservations.models import Reservation  # استيراد نموذج الحجز

class PaymentSerializer(serializers.ModelSerializer):
    reservation = serializers.PrimaryKeyRelatedField(queryset=Reservation.objects.all())  # ربط الحجز بالمدفوعات

    class Meta:
        model = Payment
        fields = ['payment_id', 'reservation', 'payment_date', 'amount_paid', 'payment_method']
