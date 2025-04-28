from django.shortcuts import render

# Create your views here.
# views.py
from rest_framework import viewsets
from .models import Inventory
from .serializers import InventorySerializer
from rest_framework.response import Response
from rest_framework.decorators import action

# ViewSet لعرض وتعديل وحذف العناصر في المخزون
class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.all()  # استرجاع جميع العناصر في المخزون
    serializer_class = InventorySerializer  # استخدم الـ Serializer الذي سننشئه

    # دالة لحذف العنصر في المخزون عبر API
    @action(detail=True, methods=['delete'])
    def delete_inventory(self, request, pk=None):
        inventory_item = self.get_object()
        inventory_item.delete()
        return Response({'message': 'Inventory item deleted successfully'}, status=204)

    # دالة لتعديل العنصر في المخزون عبر API
    @action(detail=True, methods=['put'])
    def update_inventory(self, request, pk=None):
        inventory_item = self.get_object()
        serializer = self.get_serializer(inventory_item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
