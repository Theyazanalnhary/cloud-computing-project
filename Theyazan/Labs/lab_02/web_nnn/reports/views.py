from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from .models import CrimeReport, Evidence, Investigation
from .forms import CrimeReportForm, EvidenceForm, InvestigationForm
from django.db.models import Q
from django.core.serializers.json import DjangoJSONEncoder
import json

class ReportListView(LoginRequiredMixin, ListView):
    model = CrimeReport
    template_name = 'reports/report_list.html'
    context_object_name = 'reports'
    
    def get_queryset(self):
        queryset = CrimeReport.objects.all()
        status = self.request.GET.get('status')
        priority = self.request.GET.get('priority')
        
        if status:
            queryset = queryset.filter(status=status)
        if priority:
            queryset = queryset.filter(priority=priority)
            
        return queryset.order_by('-date_reported')

class ReportCreateView(LoginRequiredMixin, CreateView):
    model = CrimeReport
    form_class = CrimeReportForm
    template_name = 'reports/report_form.html'
    success_url = reverse_lazy('reports:list')

class ReportDetailView(LoginRequiredMixin, DetailView):
    model = CrimeReport
    template_name = 'reports/report_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['evidence_form'] = EvidenceForm()
        context['investigation_form'] = InvestigationForm()
        return context

class ReportUpdateView(LoginRequiredMixin, UpdateView):
    model = CrimeReport
    form_class = CrimeReportForm
    template_name = 'reports/report_form.html'
    
    def get_success_url(self):
        return reverse_lazy('reports:detail', kwargs={'pk': self.object.pk})

class EvidenceCreateView(LoginRequiredMixin, CreateView):
    model = Evidence
    form_class = EvidenceForm
    template_name = 'reports/evidence_form.html'
    
    def form_valid(self, form):
        report = get_object_or_404(CrimeReport, pk=self.kwargs['pk'])
        form.instance.report = report
        form.instance.added_by = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('reports:detail', kwargs={'pk': self.kwargs['pk']})

class InvestigationCreateView(LoginRequiredMixin, CreateView):
    model = Investigation
    form_class = InvestigationForm
    template_name = 'reports/investigation_form.html'
    
    def form_valid(self, form):
        report = get_object_or_404(CrimeReport, pk=self.kwargs['pk'])
        form.instance.report = report
        form.instance.investigator = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('reports:detail', kwargs={'pk': self.kwargs['pk']})

class AdvancedSearchView(LoginRequiredMixin, ListView):
    model = CrimeReport
    template_name = 'reports/advanced_search.html'
    context_object_name = 'reports'
    
    def get_queryset(self):
        queryset = CrimeReport.objects.all()
        
        # البحث في العنوان والوصف
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(
                Q(title__icontains=q) |
                Q(description__icontains=q) |
                Q(location__icontains=q)
            )
        
        # تصفية حسب الحالة
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        
        # تصفية حسب الأولوية
        priority = self.request.GET.get('priority')
        if priority:
            queryset = queryset.filter(priority=priority)
        
        # تصفية حسب التاريخ
        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')
        if date_from and date_to:
            queryset = queryset.filter(
                date_reported__range=[date_from, date_to]
            )
        
        return queryset.order_by('-date_reported')

class MapView(LoginRequiredMixin, TemplateView):
    template_name = 'reports/map_view.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reports = CrimeReport.objects.filter(latitude__isnull=False, longitude__isnull=False)
        
        reports_data = [{
            'id': report.id,
            'title': report.title,
            'description': report.description,
            'latitude': float(report.latitude),
            'longitude': float(report.longitude),
            'status': report.status,
            'status_display': report.get_status_display()
        } for report in reports]
        
        context['reports_json'] = json.dumps(reports_data, cls=DjangoJSONEncoder)
        return context 