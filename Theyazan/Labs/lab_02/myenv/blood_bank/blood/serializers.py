# blood_donation/serializers.py
from rest_framework import serializers
from .models import Donor

class DonorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donor
        fields = ['id', 'name', 'blood_type', 'age', 'contact_number', 'donation_date', 'expiration_date']
