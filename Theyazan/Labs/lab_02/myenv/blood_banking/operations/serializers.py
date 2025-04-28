from rest_framework import serializers
from .models import Operation

class OperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operation
        fields = ['operation_name', 'operation_date', 'operation_type']  # إضافة نوع العملية
