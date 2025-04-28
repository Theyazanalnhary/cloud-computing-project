from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
from .models import CrimeReport

class ReportStatistics:
    @staticmethod
    def get_statistics(days=30):
        end_date = timezone.now()
        start_date = end_date - timedelta(days=days)
        
        reports = CrimeReport.objects.filter(date_reported__range=[start_date, end_date])
        
        stats = {
            'total_reports': reports.count(),
            'new_reports': reports.filter(status='new').count(),
            'solved_reports': reports.filter(status='solved').count(),
            'under_investigation': reports.filter(status='under_investigation').count(),
            
            'priority_stats': reports.values('priority').annotate(
                count=Count('id')
            ),
            
            'status_stats': reports.values('status').annotate(
                count=Count('id')
            ),
            
            'daily_reports': reports.extra(
                select={'day': 'date(date_reported)'}
            ).values('day').annotate(count=Count('id')).order_by('day'),
            
            'location_stats': reports.values('location').annotate(
                count=Count('id')
            ).order_by('-count')[:10]
        }
        
        return stats 