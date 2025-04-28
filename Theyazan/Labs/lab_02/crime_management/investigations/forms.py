from django import forms
from django.core.exceptions import ValidationError
from .models import Investigation, Crime, Suspect

class InvestigationForm(forms.ModelForm):
    crime_report_number = forms.CharField(
        label="رقم الجريمة",
        disabled=True,
        required=False,
    )

    suspect = forms.ModelChoiceField(
        queryset=Suspect.objects.none(),
        label="اختر المتهم",
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'suspect_select'}),
        required=True,
    )

    class Meta:
        model = Investigation
        fields = '__all__'
        exclude = ['crime']  # سنتعامل معه يدوياً
        labels = {
            'status': 'حالة القبض',
            'arrest_date': 'تاريخ القبض',
            'detention_date': 'تاريخ التوقيف في القسم',
            'release_date': 'تاريخ الإفراج',
            'arrest_method': 'كيفية القبض',
            'arresting_officer': 'صفة القابض',
            'transferred_to': 'نقل إلى',
            'transfer_date': 'تاريخ النقل',
            'released_on_bail': 'إفراج بضمان؟',
            'bail_guarantor': 'اسم الضامن',
            'case_closed': 'انتهت القضية؟',
            'referred_to': 'الإحالة إلى',
            'procedure_stopped': 'وقف الإجراءات؟',
            'issuing_authority': 'السلطة الآمرة',
        }
        widgets = {
            'status': forms.Select(choices=Investigation.STATUS_CHOICES, attrs={'class': 'form-select'}),
            'arrest_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'detention_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'id': 'detention_date'}),
            'release_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'id': 'release_date'}),
            'arrest_method': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'arresting_officer': forms.TextInput(attrs={'class': 'form-control'}),
            'transferred_to': forms.TextInput(attrs={'class': 'form-control'}),
            'transfer_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'released_on_bail': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'bail_guarantor': forms.TextInput(attrs={'class': 'form-control'}),
            'case_closed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'referred_to': forms.TextInput(attrs={'class': 'form-control'}),
            'procedure_stopped': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'issuing_authority': forms.TextInput(attrs={'class': 'form-control'}),
        }
    def __init__(self, *args, **kwargs):
        crime_id = kwargs.pop('crime_id', None)
        super().__init__(*args, **kwargs)

        if crime_id:
            try:
                crime = Crime.objects.get(id=crime_id)
                self.fields['crime_report_number'].initial = crime.report_number
                self.instance.crime = crime

                # تعديل الاستعلام ليعكس العلاقة ManyToMany الجديدة
                self.fields['suspect'].queryset = Suspect.objects.filter(crimes=crime)

                if self.fields['suspect'].queryset.count() == 1:
                    suspect = self.fields['suspect'].queryset.first()
                    self.fields['suspect'].initial = suspect
                    self.initial['release_date'] = suspect.release_date
                    self.initial['status'] = 'هارب' if suspect.is_fugitive else 'مقبوض'

            except Crime.DoesNotExist:
                pass

    def clean(self):
        cleaned_data = super().clean()
        detention_date = cleaned_data.get('detention_date')
        release_date = cleaned_data.get('release_date')

        # التحقق من أن تاريخ الإفراج ليس قبل تاريخ التوقيف
        if detention_date and release_date and release_date < detention_date:
            raise ValidationError("تاريخ الإفراج لا يمكن أن يكون قبل تاريخ التوقيف.")

        return cleaned_data