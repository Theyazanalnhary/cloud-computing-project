from django.shortcuts import render
from django.views.generic import ListView, UpdateView
from django.contrib.auth.mixins import UserPassesTestMixin
from reports.models import Report
from django.db.models import Count
from django.utils import timezone
from django.urls import reverse_lazy

# Create your views here.

class DashboardView(UserPassesTestMixin, ListView):
    model = Report
    template_name = 'dashboard/dashboard.html'
    context_object_name = 'reports'

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role in ['police', 'admin']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_reports'] = Report.objects.count()
        context['pending_reports'] = Report.objects.filter(status='pending').count()
        context['investigating_reports'] = Report.objects.filter(status='investigating').count()
        context['closed_reports'] = Report.objects.filter(status='closed').count()
        return context

class ReportUpdateView(UserPassesTestMixin, UpdateView):
    model = Report
    fields = ['status']
    template_name = 'dashboard/report_update.html'
    success_url = reverse_lazy('dashboard')

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role in ['police', 'admin']
