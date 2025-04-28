# blood_units/serializers.py
from rest_framework import serializers
from .models import BloodUnit

class BloodUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = BloodUnit
        fields = '__all__'
