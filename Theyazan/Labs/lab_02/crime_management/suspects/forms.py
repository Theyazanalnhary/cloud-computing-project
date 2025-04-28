from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import Suspect, Crime
from django.core.validators import RegexValidator
from django.db import IntegrityError
from django.shortcuts import get_object_or_404

class SuspectForm(forms.ModelForm):
    # حقل رقم البلاغ (للعرض فقط وغير قابل للتعديل)
    crime_report_number = forms.CharField(
        label=_("رقم البلاغ"),
        required=False,
        disabled=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    phone = forms.CharField(
        label=_("رقم الهاتف"),
        validators=[
            RegexValidator(
                regex='^[0-9]{9}$',
                message='يجب أن يتكون رقم الهاتف من 9 أرقام فقط'
            )
        ],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '7XXXXXXXX'
        })
    )

    class Meta:
        model = Suspect
        exclude = ['face_encoding', 'crimes']
        
        labels = {
            'full_name': _("الاسم الثلاثي"),
            'nickname': _("اللقب"),
            'gender': _("الجنس"),
            'nationality': _("الجنسية"),
            'country': _("البلد"),
            'age': _("العمر"),
            'residence': _("محل الإقامة"),
            'job': _("المهنة"),
            'workplace': _("جهة العمل"),
            'marital_status': _("الحالة الاجتماعية"),
            'education_level': _("المستوى التعليمي"),
            'relationship_with_victim': _("علاقة بالمجني عليه"),
            'role_in_crime': _("دور في الجريمة"),
            'previous_crimes': _("الجرائم السابقة"),
            'is_fugitive': _("هارب؟"),
            'preventive_detention_date': _("تاريخ الحبس الاحتياطي"),
            'release_date': _("تاريخ الإفراج"),
            'photo': _("صورة المتهم"),
        }

        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'أدخل الاسم الثلاثي'
            }),
            'nickname': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'أدخل اللقب (اختياري)'
            }),
            'gender': forms.Select(attrs={
                'class': 'form-select'
            }),
            'nationality': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'أدخل الجنسية'
            }),
            'country': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'أدخل البلد'
            }),
            'age': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'أدخل العمر (7-120)',
                'min': 7,
                'max': 120
            }),
            'residence': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'أدخل محل الإقامة'
            }),
            'job': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'أدخل المهنة (اختياري)'
            }),
            'workplace': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'أدخل جهة العمل (اختياري)'
            }),
            'marital_status': forms.Select(attrs={
                'class': 'form-select'
            }),
            'education_level': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'أدخل المستوى التعليمي'
            }),
            'relationship_with_victim': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'أدخل العلاقة بالمجني عليه (اختياري)'
            }),
            'role_in_crime': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'أدخل دور المتهم في الجريمة'
            }),
            'previous_crimes': forms.SelectMultiple(attrs={
                'class': 'form-select',
                'style': 'height: auto;'
            }),
            'is_fugitive': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'preventive_detention_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'release_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'photo': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
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
                
                # تعديل queryset للجرائم السابقة لاستبعاد الجريمة الحالية
                self.fields['previous_crimes'].queryset = Crime.objects.exclude(id=crime_id)
                
            except Crime.DoesNotExist:
                raise forms.ValidationError(_("الجريمة المطلوبة غير موجودة"))

    def clean_full_name(self):
        full_name = self.cleaned_data.get('full_name')
        if full_name and any(char.isdigit() for char in full_name):
            raise ValidationError(_("الاسم يجب أن يحتوي على أحرف فقط"))
        return full_name

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone and not phone.startswith('7'):
            raise ValidationError(_("رقم الهاتف يجب أن يبدأ بالرقم 7"))
        return phone

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age and (age < 7 or age > 120):
            raise ValidationError(_("يجب أن يكون العمر بين 7 و120 سنة"))
        return age

    def clean(self):
        cleaned_data = super().clean()
        full_name = cleaned_data.get('full_name')
        phone = cleaned_data.get('phone')
        age = cleaned_data.get('age')
        
        crime_id = self.initial.get('crime_id') or cleaned_data.get('crime_id')
        
        if not crime_id:
            raise ValidationError(_("لم يتم تحديد الجريمة المرتبطة بهذا المتهم."))
        
        try:
            crime = get_object_or_404(Crime, id=crime_id)
        except:
            raise ValidationError(_("الجريمة المطلوبة غير موجودة."))

        # التحقق من التكرار داخل نفس الجريمة
        if Suspect.objects.filter(
            crimes__id=crime_id,
            full_name=full_name,
            age=age,
            phone=phone
        ).exists():
            raise ValidationError(_("المتهم مسجل بالفعل في هذه الجريمة!"))

        # التحقق من التكرار في جرائم أخرى
        existing_suspect = Suspect.objects.filter(
            full_name=full_name,
            age=age,
            phone=phone
        ).first()

        if existing_suspect:
            existing_suspect.crimes.add(crime)
            raise ValidationError({
                'non_field_errors': [
                    _("المتهم '%(full_name)s' مرتبط بالفعل (رقم السجل: %(suspect_id)s). تم ربطه بالجريمة الحالية.") % {
                        'full_name': full_name,
                        'suspect_id': existing_suspect.suspect_id
                    }
                ]
            })

        # التحقق من صحة التواريخ
        preventive_detention_date = cleaned_data.get('preventive_detention_date')
        release_date = cleaned_data.get('release_date')
        
        if release_date and preventive_detention_date and release_date < preventive_detention_date:
            raise ValidationError({
                'release_date': _("تاريخ الإفراج لا يمكن أن يكون قبل تاريخ الحبس الاحتياطي")
            })
        
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        
        try:
            if commit:
                instance.save()
                
                # ربط الجريمة الحالية
                crime_id = self.initial.get('crime_id') or self.cleaned_data.get('crime_id')
                if crime_id:
                    crime = get_object_or_404(Crime, id=crime_id)
                    instance.crimes.add(crime)
                    
        except IntegrityError as e:
            raise ValidationError(_("حدث خطأ في حفظ البيانات. قد يكون المتهم مسجلاً مسبقاً.")) from e
            
        return instance
    
    
class SearchForm(forms.Form):
    query = forms.CharField(
        required=False,
        label=_("بحث بالاسم"),
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'ابحث بالاسم الكامل...'
        })
    )
    report_number = forms.CharField(
        required=False,
        label=_("رقم البلاغ"),
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'ابحق برقم البلاغ...'
        })
    )
    crime_type = forms.CharField(
        required=False,
        label=_("نوع الجريمة"),
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'ابحث بنوع الجريمة...'
        })
    )



    