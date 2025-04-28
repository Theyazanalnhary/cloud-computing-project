from django.shortcuts import render

# Create your views here.
# views.py
from rest_framework import viewsets
from .models import Payment
from .serializers import PaymentSerializer
from rest_framework.response import Response
from rest_framework.decorators import action

# ViewSet لعرض وتعديل وحذف المدفوعات
class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()  # استرجاع جميع المدفوعات
    serializer_class = PaymentSerializer  # استخدم الـ Serializer الذي سننشئه

    # دالة لحذف الدفع عبر API
    @action(detail=True, methods=['delete'])
    def delete_payment(self, request, pk=None):
        payment = self.get_object()
        payment.delete()
        return Response({'message': 'Payment deleted successfully'}, status=204)

    # دالة لتعديل الدفع عبر API
    @action(detail=True, methods=['put'])
    def update_payment(self, request, pk=None):
        payment = self.get_object()
        serializer = self.get_serializer(payment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
