# serializers.py
from rest_framework import serializers
from .models import Offer

class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ['offer_id', 'title', 'description', 'discount_percentage', 'start_date', 'end_date']
