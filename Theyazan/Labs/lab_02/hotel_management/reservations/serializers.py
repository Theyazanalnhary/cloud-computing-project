from rest_framework import serializers
from .models import Reservation


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'

    # التحقق من صحة التواريخ
    def validate(self, data):
        if data['check_in_date'] >= data['check_out_date']:
            raise serializers.ValidationError("تاريخ الدخول يجب أن يكون قبل تاريخ الخروج.")
        return data

    # حساب السعر الإجمالي عند الحفظ
    def create(self, validated_data):
        reservation = Reservation(**validated_data)
        reservation.save()
        return reservation
