from django.shortcuts import render

# Create your views here.
# views.py
from rest_framework import viewsets
from .models import Report
from .serializers import ReportSerializer
from rest_framework.response import Response
from rest_framework.decorators import action

# ViewSet لعرض وتعديل وحذف التقارير
class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()  # استرجاع جميع التقارير
    serializer_class = ReportSerializer  # استخدم الـ Serializer الذي سننشئه

    # دالة لحذف التقرير عبر API
    @action(detail=True, methods=['delete'])
    def delete_report(self, request, pk=None):
        report = self.get_object()
        report.delete()
        return Response({'message': 'Report deleted successfully'}, status=204)

    # دالة لتعديل التقرير عبر API
    @action(detail=True, methods=['put'])
    def update_report(self, request, pk=None):
        report = self.get_object()
        serializer = self.get_serializer(report, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
