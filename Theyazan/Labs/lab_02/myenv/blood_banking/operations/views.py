from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import Operation
from .serializers import OperationSerializer

class OperationListCreate(generics.ListCreateAPIView):
    queryset = Operation.objects.all()
    serializer_class = OperationSerializer
    permission_classes = [AllowAny]  # السماح لجميع المستخدمين

class OperationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Operation.objects.all()
    serializer_class = OperationSerializer
    permission_classes = [AllowAny]  # السماح لجميع المستخدمين
