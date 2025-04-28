from django import forms
from .models import Crime
from django.core.exceptions import ValidationError
import re
from datetime import date

class CrimeForm(forms.ModelForm):
    class Meta:
        model = Crime
        fields = '__all__'
        widgets = {
            'report_date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'max': date.today().isoformat()  # لا يسمح بتواريخ مستقبلية
                }
            ),
            'crime_date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'max': date.today().isoformat()
                }
            ),
            'crime_time': forms.TimeInput(attrs={'type': 'time'}),
            'description': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'minlength': '20'  # الحد الأدنى لطول الوصف
            }),
            # باقي الحقول بنفس النمط...
        }
        # التسميات كما هي...

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # إضافة التحقق من الحقول المطلوبة
        for field in self.fields:
            if self.fields[field].required:
                self.fields[field].widget.attrs['required'] = 'required'

    def clean_report_number(self):
        report_number = self.cleaned_data.get('report_number')
        
        if not report_number:
            raise ValidationError("رقم البلاغ مطلوب")
            
        if not report_number.isdigit():
            raise ValidationError("يجب أن يحتوي رقم البلاغ على أرقام فقط")
            
        # رقم البلاغ يبدأ من 1 وما فوق (أي رقم موجب)
        if int(report_number) < 1:
            raise ValidationError("يجب أن يكون رقم البلاغ أكبر من أو يساوي 1")
            
        if Crime.objects.filter(report_number=report_number).exclude(
            pk=self.instance.pk if self.instance else None
        ).exists():
            raise ValidationError("رقم البلاغ مسجل مسبقاً")
            
        return report_number

    def clean_reporter_phone(self):
        phone = self.cleaned_data.get('reporter_phone')
        
        if not phone:
            raise ValidationError("رقم الهاتف مطلوب")
            
        if not phone.isdigit():
            raise ValidationError("يجب أن يحتوي رقم الهاتف على أرقام فقط")
            
        # رقم الهاتف يجب أن يكون 9 أرقام ويبدأ بـ 7
        if len(phone) != 9:
            raise ValidationError("يجب أن يتكون رقم الهاتف من 9 أرقام")
            
        if not phone.startswith('7'):
            raise ValidationError("يجب أن يبدأ رقم الهاتف بـ 7")
            
        return phone

    def clean_reporter_name(self):
        name = self.cleaned_data.get('reporter_name')
        
        if not name:
            raise ValidationError("اسم المبلغ مطلوب")
            
        if len(name.strip()) < 3:
            raise ValidationError("يجب أن يتكون الاسم من 3 أحرف على الأقل")
            
        if re.search(r'[0-9!@#$%^&*(),.?":{}|<>]', name):
            raise ValidationError("يجب أن يحتوي الاسم على أحرف عربية فقط")
            
        return name.strip()

    def clean_crime_date(self):
        crime_date = self.cleaned_data.get('crime_date')
        
        if not crime_date:
            raise ValidationError("تاريخ الجريمة مطلوب")
            
        if crime_date > date.today():
            raise ValidationError("لا يمكن أن يكون تاريخ الجريمة في المستقبل")
            
        return crime_date

    def clean_report_date(self):
        report_date = self.cleaned_data.get('report_date')
        
        if not report_date:
            raise ValidationError("تاريخ البلاغ مطلوب")
            
        if report_date > date.today():
            raise ValidationError("لا يمكن أن يكون تاريخ البلاغ في المستقبل")
            
        return report_date

    def clean(self):
        cleaned_data = super().clean()
        
        crime_date = cleaned_data.get('crime_date')
        report_date = cleaned_data.get('report_date')
        
        if crime_date and report_date:
            if crime_date > report_date:
                raise ValidationError({
                    'crime_date': "تاريخ الجريمة لا يمكن أن يكون بعد تاريخ البلاغ"
                })
                
            if (report_date - crime_date).days > 30:
                raise ValidationError({
                    'crime_date': "يجب أن يكون تاريخ البلاغ خلال 30 يومًا من تاريخ الجريمة"
                })
        
        # تحقق إضافي للأدوات المستخدمة
        tool_used = cleaned_data.get('tool_used')
        if tool_used and len(tool_used) < 3:
            raise ValidationError({
                'tool_used': "يجب أن يحتوي وصف الأداة على 3 أحرف على الأقل"
            })
            
        return cleaned_data