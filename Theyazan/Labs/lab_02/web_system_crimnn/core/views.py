from django.shortcuts import render
from django.views.generic import TemplateView
from django.utils.translation import gettext_lazy as _

# Create your views here.

class HomePageView(TemplateView):
    template_name = "core/home.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _("الصفحة الرئيسية")
        return context

class AboutPageView(TemplateView):
    template_name = "core/about.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _("عن النظام")
        return context
