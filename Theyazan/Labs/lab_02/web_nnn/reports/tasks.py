from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .models import CrimeReport
from .statistics import ReportStatistics
from datetime import datetime, timedelta

@shared_task
def send_daily_report():
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    
    stats = ReportStatistics.get_statistics(days=1)
    
    # إعداد محتوى التقرير
    context = {
        'date': yesterday,
        'total_reports': stats['total_reports'],
        'new_reports': stats['new_reports'],
        'solved_reports': stats['solved_reports'],
        'priority_stats': stats['priority_stats']
    }
    
    # إنشاء التقرير
    html_content = render_to_string('reports/email/daily_report.html', context)
    
    # إرسال التقرير بالبريد الإلكتروني
    send_mail(
        subject=f'التقرير اليومي - {yesterday}',
        message='',
        from_email='noreply@example.com',
        recipient_list=['admin@example.com'],
        html_message=html_content
    ) 