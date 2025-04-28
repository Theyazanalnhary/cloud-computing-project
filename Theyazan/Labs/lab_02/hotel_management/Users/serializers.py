# serializers.py
from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['userid', 'fname', 'sname', 'loginname', 'email', 'phone', 'country', 'role', 'created_at', 'updated_at']
