from django.db.models import Count, Avg
from django.db.models.functions import TruncDate, TruncMonth
from .models import CrimeReport

class ReportAnalytics:
    @staticmethod
    def get_location_heatmap():
        return CrimeReport.objects.values('location').annotate(
            count=Count('id')
        ).order_by('-count')
    
    @staticmethod
    def get_monthly_trends():
        return CrimeReport.objects.annotate(
            month=TruncMonth('date_reported')
        ).values('month').annotate(
            count=Count('id')
        ).order_by('month')
    
    @staticmethod
    def get_resolution_time():
        return CrimeReport.objects.filter(
            status='solved'
        ).aggregate(
            avg_days=Avg('resolution_date' - 'date_reported')
        )
    
    @staticmethod
    def get_officer_performance():
        return CrimeReport.objects.values(
            'assigned_to__username'
        ).annotate(
            total_cases=Count('id'),
            solved_cases=Count('id', filter=models.Q(status='solved'))
        ).annotate(
            success_rate=models.F('solved_cases') * 100.0 / models.F('total_cases')
        ) 