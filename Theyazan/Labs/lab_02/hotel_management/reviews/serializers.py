# serializers.py
from rest_framework import serializers
from .models import Review
from customers.models import Customer  # استيراد نموذج العميل
from Roomes.models import Room  # استيراد نموذج الغرفة

class ReviewSerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())  # ربط التقييم بالعميل
    room = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all())  # ربط التقييم بالغرفة

    class Meta:
        model = Review
        fields = ['review_id', 'customer', 'room', 'rating', 'comments', 'review_date']
