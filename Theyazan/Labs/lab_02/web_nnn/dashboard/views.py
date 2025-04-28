from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.shortcuts import render
from reports.models import CrimeReport
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta

class DashboardHomeView(LoginRequiredMixin, ListView):
    template_name = 'dashboard/home.html'
    context_object_name = 'reports'
    
    def get_queryset(self):
        if self.request.user.user_type == 'admin':
            return CrimeReport.objects.all()
        return CrimeReport.objects.filter(assigned_to=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # إحصائيات عامة
        context['total_reports'] = CrimeReport.objects.count()
        context['new_reports'] = CrimeReport.objects.filter(status='new').count()
        context['solved_reports'] = CrimeReport.objects.filter(status='solved').count()
        
        # تقارير حسب الأولوية
        context['priority_stats'] = CrimeReport.objects.values('priority').annotate(
            count=Count('id')
        )
        
        # تقارير الأسبوع الماضي
        week_ago = timezone.now() - timedelta(days=7)
        context['recent_reports'] = CrimeReport.objects.filter(
            date_reported__gte=week_ago
        ).order_by('-date_reported')
        
        return context 