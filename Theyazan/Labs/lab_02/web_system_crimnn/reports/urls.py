
from django.urls import path
from . import views

app_name = 'reports'  # تحديد namespace للتطبيق

urlpatterns = [
    path('report/create/', views.CreateReportView.as_view(), name='report_create'),
    path('report/list/', views.ReportListView.as_view(), name='report_list'),
    path('report/track/', views.ReportTrackingView.as_view(), name='track_report'),
    path('report/<int:pk>/', views.ReportDetailView.as_view(), name='report_detail'),
]