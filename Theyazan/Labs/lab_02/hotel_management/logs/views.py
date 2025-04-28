from django.shortcuts import render

# Create your views here.
# views.py
from rest_framework import viewsets
from .models import Log
from .serializers import LogSerializer
from rest_framework.response import Response
from rest_framework.decorators import action

# ViewSet لعرض وتعديل وحذف السجلات
class LogViewSet(viewsets.ModelViewSet):
    queryset = Log.objects.all()  # استرجاع جميع السجلات
    serializer_class = LogSerializer  # استخدم الـ Serializer الذي سننشئه

    # دالة لحذف السجل عبر API
    @action(detail=True, methods=['delete'])
    def delete_log(self, request, pk=None):
        log = self.get_object()
        log.delete()
        return Response({'message': 'Log deleted successfully'}, status=204)

    # دالة لتعديل السجل عبر API
    @action(detail=True, methods=['put'])
    def update_log(self, request, pk=None):
        log = self.get_object()
        serializer = self.get_serializer(log, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
