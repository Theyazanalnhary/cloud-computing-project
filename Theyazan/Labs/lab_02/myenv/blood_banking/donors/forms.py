
from django import forms
from .models import Donor
from datetime import date


class DonorForm(forms.ModelForm):
    class Meta:
        model = Donor
        fields = [
            'full_name',        # الاسم الكامل
            'date_of_birth',    # تاريخ الميلاد
            'gender',           # الجنس
            'blood_type',       # فصيلة الدم
            'phone_number',     # رقم الهاتف
            'address',          # العنوان
            'health_status',    # الحالة الصحية
            'last_donation_date' # تاريخ آخر تبرع
        ]

        # تخصيص واجهة الإدخال
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'last_donation_date': forms.DateInput(attrs={'type': 'date'}),
            'gender': forms.Select(choices=Donor.GENDER_CHOICES),
            'blood_type': forms.Select(choices=Donor.BLOOD_TYPE_CHOICES),
            'health_status': forms.Select(choices=Donor.HEALTH_STATUS_CHOICES),
        }

    def clean_date_of_birth(self):
        """التحقق من أن عمر المتبرع لا يقل عن 18 عامًا"""
        dob = self.cleaned_data['date_of_birth']
        age = (date.today() - dob).days // 365
        if age < 18:
            raise forms.ValidationError("يجب أن يكون عمر المتبرع 18 عامًا على الأقل.")
        return dob

    def clean_phone_number(self):
        """التحقق من صحة رقم الهاتف"""
        phone = self.cleaned_data['phone_number']
        if not phone.isdigit():
            raise forms.ValidationError("يجب أن يحتوي رقم الهاتف على أرقام فقط.")
        if len(phone) < 10 or len(phone) > 15:
            raise forms.ValidationError("رقم الهاتف يجب أن يكون بين 10 و 15 رقماً.")
        return phone

    def clean_last_donation_date(self):
        """التحقق من أن تاريخ آخر تبرع صالح"""
        last_date = self.cleaned_data.get('last_donation_date')
        if last_date and last_date > date.today():
            raise forms.ValidationError("تاريخ آخر تبرع لا يمكن أن يكون في المستقبل.")
        return last_date
