from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CrimeReportForm, ReportImageForm
from .models import CrimeReport, ReportImage

@login_required
def submit_report(request):
    if request.method == 'POST':
        report_form = CrimeReportForm(request.POST)
        image_form = ReportImageForm(request.POST, request.FILES)
        
        if report_form.is_valid():
            report = report_form.save(commit=False)
            if not report.is_anonymous:
                report.reporter = request.user
            report.save()

            if 'images' in request.FILES:
                for image in request.FILES.getlist('images'):
                    ReportImage.objects.create(report=report, image=image)

            messages.success(request, f'تم تسجيل البلاغ بنجاح. رقم المتابعة: {report.reference_number}')
            return redirect('track_report', ref_number=report.reference_number)
    else:
        report_form = CrimeReportForm()
        image_form = ReportImageForm()

    return render(request, 'reports/submit_report.html', {
        'report_form': report_form,
        'image_form': image_form
    })

def track_report(request, ref_number=None):
    report = None
    if ref_number:
        report = CrimeReport.objects.filter(reference_number=ref_number).first()
    
    return render(request, 'reports/track_report.html', {'report': report}) 