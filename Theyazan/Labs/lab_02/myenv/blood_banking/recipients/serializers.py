# recipients/serializers.py

from rest_framework import serializers
from .models import Recipient

class RecipientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipient
        fields = ['name', 'blood_type', 'age', 'request_date', 'quantity']
