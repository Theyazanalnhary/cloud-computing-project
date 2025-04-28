# serializers.py
from rest_framework import serializers
from .models import Log

class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log
        fields = '__all__'  # لتضمين جميع الحقول في النموذج
