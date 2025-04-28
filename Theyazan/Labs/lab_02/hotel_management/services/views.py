from django.shortcuts import render

# Create your views here.
# views.py
from rest_framework import viewsets
from .models import Service
from .serializers import ServiceSerializer

class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()  # استرجاع جميع الخدمات
    serializer_class = ServiceSerializer  # استخدام الـ Serializer الذي تم إنشاؤه
