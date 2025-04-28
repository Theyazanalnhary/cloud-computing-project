# blood_tests/serializers.py

from rest_framework import serializers
from .models import BloodTest

class BloodTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = BloodTest
        fields = '__all__'
