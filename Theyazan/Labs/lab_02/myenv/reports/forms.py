from django import forms
from .models import CrimeReport

class CrimeReportForm(forms.ModelForm):
    class Meta:
        model = CrimeReport
        fields = ['crime_type', 'location', 'description', 'is_anonymous']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class ReportImageForm(forms.Form):
    images = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}),
        required=False
    ) 