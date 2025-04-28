from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Report, ReportMedia

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = [ 'location', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class ReportMediaForm(forms.ModelForm):
    class Meta:
        model = ReportMedia
        fields = ['file']
