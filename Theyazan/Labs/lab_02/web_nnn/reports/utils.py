import csv
from django.http import HttpResponse
from openpyxl import Workbook
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from io import BytesIO

def export_reports_csv(queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="reports.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['العنوان', 'الوصف', 'الموقع', 'تاريخ البلاغ', 'الحالة', 'الأولوية'])
    
    for report in queryset:
        writer.writerow([
            report.title,
            report.description,
            report.location,
            report.date_reported,
            report.get_status_display(),
            report.get_priority_display()
        ])
    
    return response

def export_reports_excel(queryset):
    wb = Workbook()
    ws = wb.active
    ws.title = "التقارير"
    
    headers = ['العنوان', 'الوصف', 'الموقع', 'تاريخ البلاغ', 'الحالة', 'الأولوية']
    ws.append(headers)
    
    for report in queryset:
        ws.append([
            report.title,
            report.description,
            report.location,
            report.date_reported,
            report.get_status_display(),
            report.get_priority_display()
        ])
    
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="reports.xlsx"'
    wb.save(response)
    return response 