from django import forms
from django.core.exceptions import ValidationError
from .models import Prosecution, Crime, Investigation
from django.utils.translation import gettext_lazy as _

class ProsecutionForm(forms.ModelForm):
    crime_report_number = forms.CharField(
        label=_("رقم البلاغ/الجريمة"),
        disabled=True,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    investigation = forms.ModelChoiceField(
        queryset=Investigation.objects.none(),
        label=_("إجراء التحري"),
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=True
    )

    class Meta:
        model = Prosecution
        fields = '__all__'
        exclude = ['crime', 'prosecution_id']
        
        widgets = {
            'prosecutor_office': forms.TextInput(attrs={'class': 'form-control'}),
            'case_number': forms.TextInput(attrs={'class': 'form-control'}),
            'submission_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'prosecutor_decisions': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'referral_to_court_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'court_procedures': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'verdict': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'sentence_execution': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        crime_id = kwargs.pop('crime_id', None)
        super().__init__(*args, **kwargs)
        
        if crime_id:
            try:
                crime = Crime.objects.get(id=crime_id)
                self.fields['crime_report_number'].initial = crime.report_number
                self.instance.crime = crime
                
                # تحديث قائمة إجراءات التحري المرتبطة بالجريمة
                investigations = Investigation.objects.filter(crime=crime)
                self.fields['investigation'].queryset = investigations
                
                if investigations.count() == 1:
                    self.initial['investigation'] = investigations.first()
                    
            except Crime.DoesNotExist:
                raise ValidationError(_("الجريمة المحددة غير موجودة"))

    def clean(self):
        cleaned_data = super().clean()
        crime = getattr(self.instance, 'crime', None)
        investigation = cleaned_data.get('investigation')
        
        if crime and investigation:
            # التحقق من أن إجراء التحري مرتبط بالجريمة الصحيحة
            if investigation.crime != crime:
                raise ValidationError({
                    'investigation': _("إجراء التحري المحدد غير مرتبط بالجريمة الحالية")
                })
            
            # التحقق من عدم تكرار إجراء النيابة لنفس إجراء التحري
            existing = Prosecution.objects.filter(
                crime=crime,
                investigation=investigation
            ).exclude(pk=self.instance.pk if self.instance else None)
            
            if existing.exists():
                raise ValidationError({
                    'investigation': _("هذا إجراء التحري لديه بالفعل إجراء نيابة مسجل لهذه الجريمة!")
                })
        
        return cleaned_data