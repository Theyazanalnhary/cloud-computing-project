from django import forms
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from .models import Damage, Crime

class DamageForm(forms.ModelForm):
    crime_report_number = forms.CharField(
        label="رقم الجريمة",
        disabled=True,
        required=False,
    )
    
    class Meta:
        model = Damage
        fields = '__all__'
        exclude = ['crime']  # نستثني حقل crime لأنه سنتعامل معه يدوياً
        labels = {
            'damage_type': 'نوع الضرر',
            'male_deaths': 'عدد وفيات الذكور',
            'female_deaths': 'عدد وفيات الإناث',
            'male_injuries': 'عدد إصابات الذكور',
            'female_injuries': 'عدد إصابات الإناث',
            'material_damage_description': 'وصف الضرر المادي',
        }
        widgets = {
            'material_damage_description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'أدخل تفاصيل الضرر المادي...'}),
        }

    def __init__(self, *args, **kwargs):
        self.crime = kwargs.pop('crime', None)
        crime_id = kwargs.pop('crime_id', None)
        super().__init__(*args, **kwargs)

        # جلب بيانات الجريمة إما من crime_id أو من self.crime
        if crime_id:
            self.crime = Crime.objects.get(id=crime_id)
        
        if self.crime:
            self.fields['crime_report_number'].initial = self.crime.report_number
        else:
            raise ValueError("يجب توفير معرف الجريمة أو كائن الجريمة")

    def clean(self):
        cleaned_data = super().clean()
        
        if not self.crime:
            raise ValidationError("لم يتم تحديد الجريمة المرتبطة بالضرر")
        
        damage_type = cleaned_data.get('damage_type')
        male_deaths = cleaned_data.get('male_deaths', 0)
        female_deaths = cleaned_data.get('female_deaths', 0)
        
        # التحقق من صحة الحقول
        if damage_type and any(char.isdigit() for char in damage_type):
            raise ValidationError("نوع الضرر يجب أن يكون نصًا فقط.")
        
        # التحقق من التكرار
        exists = Damage.objects.filter(
            crime=self.crime,
            damage_type=damage_type,
            male_deaths=male_deaths,
            female_deaths=female_deaths
        ).exclude(pk=self.instance.pk if self.instance else None).exists()
        
        if exists:
            raise ValidationError(
                "هذه البيانات مسجلة مسبقاً لنفس الجريمة! "
                "(نفس نوع الضرر وعدد الوفيات)"
            )
        
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.crime = self.crime  # تعيين الجريمة هنا
        
        if commit:
            try:
                instance.save()
            except IntegrityError as e:
                if 'unique_together' in str(e).lower():
                    raise ValidationError("هذه البيانات مسجلة مسبقاً لنفس الجريمة!")
                raise
        return instance