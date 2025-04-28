from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import CrimeReportSerializer, EvidenceSerializer, InvestigationSerializer
from reports.models import CrimeReport, Evidence, Investigation

class CrimeReportViewSet(viewsets.ModelViewSet):
    queryset = CrimeReport.objects.all()
    serializer_class = CrimeReportSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_superuser:
            queryset = queryset.filter(assigned_to=self.request.user)
        return queryset

class EvidenceViewSet(viewsets.ModelViewSet):
    queryset = Evidence.objects.all()
    serializer_class = EvidenceSerializer
    permission_classes = [IsAuthenticated]

class InvestigationViewSet(viewsets.ModelViewSet):
    queryset = Investigation.objects.all()
    serializer_class = InvestigationSerializer
    permission_classes = [IsAuthenticated] 