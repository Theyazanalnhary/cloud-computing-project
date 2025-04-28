from django.shortcuts import render
from django.views.generic import CreateView, DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Report
from .forms import ReportForm
import uuid

# Create your views here.

from django.contrib import messages

class CreateReportView(CreateView):
    model = Report
    form_class = ReportForm
    template_name = 'reports/create_report.html'
    success_url = reverse_lazy('reports:report_list')  # توجيه المستخدم إلى قائمة البلاغات بعد الإنشاء

    def form_valid(self, form):
        form.instance.reference_number = str(uuid.uuid4().hex[:8])
        if self.request.user.is_authenticated:
            form.instance.reporter = self.request.user
        else:
            form.instance.is_anonymous = True
        messages.success(self.request, 'تم تقديم البلاغ بنجاح!')  # إضافة رسالة نجاح
        return super().form_valid(form)

class ReportDetailView(DetailView):
    model = Report
    template_name = 'reports/report_detail.html'
    context_object_name = 'report'

class ReportTrackingView(ListView):
    model = Report
    template_name = 'reports/track_report.html'
    context_object_name = 'reports'

    def get_queryset(self):
        reference_number = self.request.GET.get('reference_number')
        if reference_number:
            return Report.objects.filter(reference_number=reference_number)
        return Report.objects.none()


from django.contrib.auth.mixins import LoginRequiredMixin

class ReportListView(LoginRequiredMixin, ListView):
    model = Report
    template_name = 'reports/report_list.html'
    context_object_name = 'reports'

    def get_queryset(self):
        return Report.objects.filter(reporter=self.request.user)