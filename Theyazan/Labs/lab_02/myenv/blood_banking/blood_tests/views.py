# blood_tests/views.py

from rest_framework import generics
from .models import BloodTest
from .serializers import BloodTestSerializer

class BloodTestListCreate(generics.ListCreateAPIView):
    queryset = BloodTest.objects.all()
    serializer_class = BloodTestSerializer

class BloodTestDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = BloodTest.objects.all()
    serializer_class = BloodTestSerializer
