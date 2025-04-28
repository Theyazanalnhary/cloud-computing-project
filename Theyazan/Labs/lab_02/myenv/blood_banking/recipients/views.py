from rest_framework.permissions import AllowAny
from rest_framework import generics  # تأكد من استيراد generics
from .models import Recipient
from .serializers import RecipientSerializer
class RecipientListCreate(generics.ListCreateAPIView):
    queryset = Recipient.objects.all()
    serializer_class = RecipientSerializer
    permission_classes = [AllowAny]  # السماح لأي مستخدم

class RecipientDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Recipient.objects.all()
    serializer_class = RecipientSerializer
    permission_classes = [AllowAny]  # السماح لأي مستخدم
