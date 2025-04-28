from django import forms
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from .models import Victim, Crime

class VictimForm(forms.ModelForm):
    # حقل رقم الجريمة (للعرض فقط وغير قابل للتعديل)
    crime_report_number = forms.CharField(
        label="رقم الجريمة",
        required=False,
        disabled=True,
    )

    class Meta:
        model = Victim
        fields = '__all__'
        exclude = ['crimes']  # استبعاد الحقل crimes لأنه يتم التعامل معه يدويًا

        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'nickname': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'nationality': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'residence': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'pattern': '[0-9]*',
                'inputmode': 'numeric'
            }),
            'job': forms.TextInput(attrs={'class': 'form-control'}),
            'workplace': forms.TextInput(attrs={'class': 'form-control'}),
            'education_level': forms.TextInput(attrs={'class': 'form-control'}),
            'marital_status': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        crime_id = kwargs.pop('crime_id', None)
        super().__init__(*args, **kwargs)

        if crime_id:
            try:
                crime = Crime.objects.get(id=crime_id)
                self.fields['crime_report_number'].initial = crime.report_number
                self.initial['crime_id'] = crime.id
                self.fields['crime_id'] = forms.CharField(
                    widget=forms.HiddenInput(),
                    initial=crime.id
                )
            except Crime.DoesNotExist:
                raise ValidationError("الجريمة المطلوبة غير موجودة.")

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone:
            raise ValidationError("رقم الهاتف مطلوب.")
        if not phone.isdigit():
            raise ValidationError("يجب أن يحتوي رقم الهاتف على أرقام فقط.")
        if len(phone) != 9:
            raise ValidationError("يجب أن يتكون رقم الهاتف من 9 أرقام.")
        if not phone.startswith('7'):
            raise ValidationError("يجب أن يبدأ رقم الهاتف بـ 7.")
        return phone

    def clean(self):
        cleaned_data = super().clean()
        full_name = cleaned_data.get('full_name')
        age = cleaned_data.get('age')
        phone = cleaned_data.get('phone')
        
        # الحصول على crime_id من البيانات الأولية أو المنشأة
        crime_id = self.initial.get('crime_id') or cleaned_data.get('crime_id')
        
        if not crime_id:
            raise ValidationError("لم يتم تحديد الجريمة المرتبطة بهذا المجني عليه.")
        
        try:
            crime = get_object_or_404(Crime, id=crime_id)
        except:
            raise ValidationError("الجريمة المطلوبة غير موجودة.")

        # التحقق من التكرار داخل نفس الجريمة
        if Victim.objects.filter(
            crimes__id=crime_id,
            full_name=full_name,
            age=age,
            phone=phone
        ).exists():
            raise ValidationError("المجني عليه مسجل بالفعل في هذه الجريمة!")

        # التحقق من التكرار في جرائم أخرى
        existing_victim = Victim.objects.filter(
            full_name=full_name,
            age=age,
            phone=phone
        ).first()

        if existing_victim:
            existing_victim.crimes.add(crime)
            raise ValidationError({
                'non_field_errors': [
                    f"المجني عليه '{full_name}' مرتبط بالفعل برقم بلاغ سابق "
                    f"(رقم السجل: {existing_victim.victim_id}). "
                    f"تم ربطه بالجريمة الحالية."
                ]
            })

        return cleaned_data