from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('report/<int:pk>/update/', views.ReportUpdateView.as_view(), name='report_update'),
] 