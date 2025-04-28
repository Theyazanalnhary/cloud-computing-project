from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
from reports.models import CrimeReport, ReportUpdate
from .forms import ReportUpdateForm, ReportFilterForm
import json

def is_security(user):
    return user.is_authenticated and user.is_security()

@login_required
@user_passes_test(is_security)
def dashboard_home(request):
    # إحصائيات عامة
    total_reports = CrimeReport.objects.count()
    pending_reports = CrimeReport.objects.filter(status='pending').count()
    investigating_reports = CrimeReport.objects.filter(status='investigating').count()
    closed_reports = CrimeReport.objects.filter(status='closed').count()
    
    # البلاغات حسب النوع
    reports_by_type = CrimeReport.objects.values('crime_type').annotate(count=Count('id'))
    
    # البلاغات الأخيرة
    recent_reports = CrimeReport.objects.order_by('-date_reported')[:10]
    
    context = {
        'total_reports': total_reports,
        'pending_reports': pending_reports,
        'investigating_reports': investigating_reports,
        'closed_reports': closed_reports,
        'reports_by_type': reports_by_type,
        'recent_reports': recent_reports,
    }
    
    return render(request, 'dashboard/home.html', context)

@login_required
@user_passes_test(is_security)
def reports_list(request):
    reports = CrimeReport.objects.all().order_by('-date_reported')
    filter_form = ReportFilterForm(request.GET)
    
    if filter_form.is_valid():
        if filter_form.cleaned_data.get('status'):
            reports = reports.filter(status=filter_form.cleaned_data['status'])
        if filter_form.cleaned_data.get('crime_type'):
            reports = reports.filter(crime_type=filter_form.cleaned_data['crime_type'])
        if filter_form.cleaned_data.get('date_from'):
            reports = reports.filter(date_reported__gte=filter_form.cleaned_data['date_from'])
        if filter_form.cleaned_data.get('date_to'):
            reports = reports.filter(date_reported__lte=filter_form.cleaned_data['date_to'])

    return render(request, 'dashboard/reports_list.html', {
        'reports': reports,
        'filter_form': filter_form
    })

@login_required
@user_passes_test(is_security)
def statistics(request):
    # إحصائيات عامة
    total_reports = CrimeReport.objects.count()
    reports_by_status = CrimeReport.objects.values('status').annotate(count=Count('id'))
    reports_by_type = CrimeReport.objects.values('crime_type').annotate(count=Count('id'))
    
    # إحصائيات حسب الوقت
    today = timezone.now()
    last_week = today - timedelta(days=7)
    last_month = today - timedelta(days=30)
    
    reports_by_day = CrimeReport.objects.filter(
        date_reported__gte=last_week
    ).extra(
        select={'day': 'date(date_reported)'}
    ).values('day').annotate(count=Count('id')).order_by('day')

    # تحويل البيانات لتنسيق مناسب للرسم البياني
    chart_data = {
        'labels': [str(item['day']) for item in reports_by_day],
        'data': [item['count'] for item in reports_by_day]
    }

    return render(request, 'dashboard/statistics.html', {
        'total_reports': total_reports,
        'reports_by_status': reports_by_status,
        'reports_by_type': reports_by_type,
        'chart_data': json.dumps(chart_data)
    })

@login_required
@user_passes_test(is_security)
def export_reports(request):
    import csv
    from django.http import HttpResponse
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="reports.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['رقم البلاغ', 'نوع الجريمة', 'الموقع', 'التاريخ', 'الحالة'])
    
    reports = CrimeReport.objects.all()
    for report in reports:
        writer.writerow([
            report.id,
            report.get_crime_type_display(),
            report.location,
            report.date_reported,
            report.get_status_display()
        ])
    
    return response

@login_required
@user_passes_test(is_security)
def update_status(request, report_id):
    report = get_object_or_404(CrimeReport, id=report_id)
    if request.method == 'POST':
        form = ReportUpdateForm(request.POST)
        if form.is_valid():
            update = form.save(commit=False)
            update.report = report
            update.updated_by = request.user
            update.save()
            
            report.status = update.status
            report.save()
            
            messages.success(request, 'تم تحديث حالة البلاغ بنجاح')
            return redirect('dashboard:report_detail', report_id=report.id)
    
    return redirect('dashboard:report_detail', report_id=report.id)

@login_required
@user_passes_test(is_security)
def report_detail(request, report_id):
    report = get_object_or_404(CrimeReport, id=report_id)
    update_form = ReportUpdateForm()
    
    return render(request, 'dashboard/report_detail.html', {
        'report': report,
        'update_form': update_form
    }) 