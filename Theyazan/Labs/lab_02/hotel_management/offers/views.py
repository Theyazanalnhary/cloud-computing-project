from django.shortcuts import render

# Create your views here.
# views.py
from rest_framework import viewsets
from .models import Offer
from .serializers import OfferSerializer
from rest_framework.response import Response
from rest_framework.decorators import action

# ViewSet لعرض وتعديل وحذف العروض
class OfferViewSet(viewsets.ModelViewSet):
    queryset = Offer.objects.all()  # استرجاع جميع العروض
    serializer_class = OfferSerializer  # استخدم الـ Serializer الذي سننشئه

    # دالة لحذف العرض عبر API
    @action(detail=True, methods=['delete'])
    def delete_offer(self, request, pk=None):
        offer = self.get_object()
        offer.delete()
        return Response({'message': 'Offer deleted successfully'}, status=204)

    # دالة لتعديل العرض عبر API
    @action(detail=True, methods=['put'])
    def update_offer(self, request, pk=None):
        offer = self.get_object()
        serializer = self.get_serializer(offer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
